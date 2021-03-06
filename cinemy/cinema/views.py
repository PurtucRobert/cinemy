from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from ratelimit.decorators import ratelimit
from django.contrib.auth.decorators import login_required
from .models import Cinema, Movie, PlayingTime, Reservation, Seat, Hall
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.views.generic import DetailView
from django.utils.decorators import method_decorator
import csv
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from base64 import urlsafe_b64decode


@login_required()
@ratelimit(key="ip", rate="30/m", block=True)
def select_cinema(request):
    if request.method == "GET":
        cinemas = Cinema.objects.all()
        return render(request, "cinema/select_cinema.html", {"cinemas": cinemas})


@login_required()
@ratelimit(key="ip", rate="30/m", block=True)
def select_movie(request, cinema_id):
    if request.method == "GET":
        movie_time_frames = PlayingTime.objects.filter(
            assigned_hall__in=Hall.objects.filter(cinema=cinema_id),
            start_time__gt=timezone.now(),
        )
        if movie_time_frames:
            movies = set(
                [time_frame.assigned_movie for time_frame in movie_time_frames]
            )
        else:
            movies = []
        return render(
            request,
            "cinema/select_movie.html",
            {"movies": movies},
        )
    if request.method == "POST":
        movie_id = request.POST["movie_id"]
        return redirect("select_timeframe", movie_id=movie_id, cinema_id=cinema_id)


@login_required()
@ratelimit(key="ip", rate="30/m", block=True)
def select_timeframe(request, movie_id, cinema_id):
    if request.method == "GET":
        time_frames = PlayingTime.objects.filter(
            assigned_movie=movie_id,
            assigned_hall__in=Hall.objects.filter(cinema=cinema_id),
            start_time__gt=timezone.now(),
        )
        return render(
            request, "cinema/select_timeframe.html", {"time_frames": time_frames}
        )


@login_required()
@ratelimit(key="ip", rate="30/m", block=True)
def select_seats(request, pk):
    if request.method == "GET":
        hall = Hall.objects.get(pk=PlayingTime.objects.get(pk=pk).assigned_hall.id)
        reservations = Reservation.objects.filter(
            reserved_time=PlayingTime.objects.get(pk=pk)
        )
        reserved_seats = [item.seat.name for item in reservations]
        seats_letters = []
        for i in range(65, 65 + hall.rows):
            seats_letters.append(chr(i))
        return render(
            request,
            "cinema/select_seats.html",
            {
                "reserved_seats": reserved_seats,
                "rows": range(1, hall.seats_per_row + 1),
                "seats_letters": seats_letters,
            },
        )
    if request.method == "POST":
        seats = request.POST.getlist("seats")
        playing_time = PlayingTime.objects.get(pk=pk)
        user = User.objects.get(username=request.user)
        reservations = []
        for seat in seats:
            reservations.append(
                Reservation(
                    seat=Seat.objects.get(
                        name=seat, hall=playing_time.assigned_hall.id
                    ),
                    reservation_name=user,
                    reserved_time=playing_time,
                )
            )
        try:
            existing_ids = list(
                Reservation.objects.filter(
                    reserved_time=playing_time, reservation_name=user
                ).values_list("id", flat=True)
            )
            Reservation.objects.bulk_create(reservations)
            new_ids = list(
                Reservation.objects.exclude(id__in=existing_ids).values_list(
                    "id", flat=True
                )
            )
            ids_string = ",".join([str(res_id) for res_id in new_ids])
            encoded_ids = urlsafe_base64_encode(force_bytes(ids_string))
        except IntegrityError:
            messages.success(request, (f"Seat {seat} is already reserved"))
            return redirect(request.path)
        else:
            new_ids = list(
                Reservation.objects.exclude(id__in=existing_ids).values_list(
                    "id", flat=True
                )
            )
            ids_string = ",".join([str(res_id) for res_id in new_ids])
            encoded_ids = urlsafe_base64_encode(force_bytes(ids_string))
            email_subject = f"Your booking for: {playing_time.assigned_movie.name} was completed successfully"
            seats_names = " ".join(seats)
            current_site = get_current_site(request)
            email_message = render_to_string(
                "cinema/ticket_booking_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": encoded_ids,
                    "seats": seats_names,
                    "hall_name": playing_time.assigned_hall.name,
                    "movie_name": playing_time.assigned_movie.name,
                },
            )
            send_mail(
                email_subject,
                email_message,
                settings.CONTACT_EMAIL,
                [user.email],
            )
        return redirect("front_page")


@method_decorator(ratelimit(key="ip", rate="30/m", block=True), name="get")
class MovieDetail(DetailView):
    model = Movie


@login_required()
@ratelimit(key="ip", rate="30/m", block=True)
def reservations_per_user(request, pk):
    user = User.objects.get(pk=pk)
    reservations = Reservation.objects.filter(reservation_name=user)
    if request.method == "GET":
        return render(
            request, "cinema/reservations.html", {"reservations": reservations}
        )
    if request.method == "POST" and "download_reservations" in request.POST:
        file_name = f"reservations_{user.username}.csv"
        response = HttpResponse(
            headers={"Content-Disposition": f"attachment; filename={file_name}"},
            content_type="text/csv",
        )
        writer = csv.writer(response)
        writer.writerow(
            ["Reservation ID", "User", "Movie", "Start time", "Hall", "Seat"]
        )
        for reservation in reservations:
            writer.writerow(
                [
                    reservation.id,
                    reservation.reservation_name,
                    reservation.reserved_time.assigned_movie.name,
                    reservation.reserved_time.start_time,
                    reservation.reserved_time.assigned_hall.name,
                    reservation.seat.name,
                ]
            )
        return response

    elif request.method == "POST" and "confirm_reservations" in request.POST:
        checked_reservations = request.POST.getlist("reservations_check")
        Reservation.objects.filter(pk__in=checked_reservations).update(confirmed=True)
        return render(
            request, "cinema/reservations.html", {"reservations": reservations}
        )


@login_required()
@ratelimit(key="ip", rate="30/m", block=True)
def confirm_reservations(request, uidb64):
    uidb64_padded = uidb64 + "=" * (-len(uidb64) % 4)
    ids = force_str(urlsafe_b64decode(uidb64_padded)).split(",")
    Reservation.objects.filter(id__in=ids).update(confirmed=True)
    return HttpResponse("Thank you for confirming your reservations")
