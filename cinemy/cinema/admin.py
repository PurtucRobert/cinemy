import csv
from django.db import IntegrityError
import requests
from django.core.files.base import ContentFile
from django import forms
from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path
from cinema.models import Movie, Cinema, Hall, Seat, Reservation, PlayingTime
from nested_inline.admin import NestedTabularInline, NestedModelAdmin
from io import TextIOWrapper


class ReservationInline(NestedTabularInline):
    model = Reservation


class SeatInline(NestedTabularInline):
    model = Seat
    extra = 0
    inlines = (ReservationInline,)


class HallInline(NestedTabularInline):
    model = Hall
    extra = 0
    inlines = (SeatInline,)


class PlayingTimeInline(NestedTabularInline):
    model = PlayingTime


@admin.register(Cinema)
class CinemaAdmin(NestedModelAdmin):
    inlines = (HallInline,)


@admin.register(Hall)
class HallAdmin(NestedModelAdmin):
    inlines = (SeatInline,)


@admin.register(Reservation)
class ReservationAdmin(NestedModelAdmin):
    exclude = ("is_reserved",)


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


@admin.register(Movie)
class MovieAdmin(NestedModelAdmin):
    inlines = (PlayingTimeInline,)
    exclude = ("imdb_link",)
    change_list_template = "admin/movie_admin.html"

    def get_urls(self):
        urls = super().get_urls()
        defined_urls = [
            path("import_csv/", self.import_csv),
        ]
        return defined_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            file = TextIOWrapper(
                request.FILES["csv_file"].file, encoding=request.encoding
            )
            movies_from_csv = csv.DictReader(file)
            movies = []
            for movie_from_csv in movies_from_csv:
                try:
                    created_movie = Movie(**movie_from_csv)
                    name = movie_from_csv["poster"].split("/")[-1]
                    response = requests.get(created_movie.poster)
                    if response.status_code == 200:
                        created_movie.poster.save(
                            name, ContentFile(response.content), save=False
                        )
                except requests.exceptions.MissingSchema:
                    pass
                except IntegrityError:
                    pass
                else:
                    movies.append(created_movie)
            Movie.objects.bulk_create(movies)
            return redirect("..")
        if request.method == "GET":
            form = CsvImportForm()
            payload = {"form": form}
            return render(request, "admin/csv_form.html", payload)


@admin.register(PlayingTime)
class PlayingTime(NestedModelAdmin):
    readonly_fields = ("end_time",)
    exclude = ("end_time",)


admin.site.register(Seat)
