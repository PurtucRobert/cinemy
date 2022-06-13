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
            assigned_hall__in=Hall.objects.filter(cinema=cinema_id)
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
            Reservation.objects.bulk_create(reservations)
        except IntegrityError:
            messages.success(request, (f"Seat {seat} is already reserved"))
            return redirect(request.path)
        else:
            email_subject = f"Your booking for: {playing_time.assigned_movie.name} was completed successfully"
            seats_names = " ".join(seats)
            email_message = render_to_string(
                "cinema/ticket_booking_email.html",
                {
                    "user": user,
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
    template_name = "cinema/movie_details.html"


@login_required()
@ratelimit(key="ip", rate="30/m", block=True)
def reservations_per_user(request, pk):
    user = User.objects.get(pk=pk)
    reservations = Reservation.objects.filter(reservation_name=user)
    file_name = f"reservations_{user.username}.csv"
    response = HttpResponse(
        headers={"Content-Disposition": f"attachment; filename={file_name}"},
        content_type="text/csv",
    )
    writer = csv.writer(response)
    writer.writerow(["User", "Movie", "Start time", "Hall", "Seat"])
    for reservation in reservations:
        writer.writerow(
            [
                reservation.reservation_name,
                reservation.reserved_time.assigned_movie.name,
                reservation.reserved_time.start_time,
                reservation.reserved_time.assigned_hall.name,
                reservation.seat.name,
            ]
        )
    return response
