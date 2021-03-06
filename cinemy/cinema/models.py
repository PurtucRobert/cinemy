from django.db import models
from django.utils.html import format_html
from django.contrib.auth.models import User
from datetime import datetime, timedelta

# Create your models here.


class Movie(models.Model):
    name = models.CharField(max_length=100)
    poster = models.ImageField(upload_to="posters/", blank=True, null=True)
    description = models.TextField()
    imdb_link = models.CharField(max_length=100)
    imdb_id = models.CharField(max_length=100)
    trailer_url = models.CharField(max_length=100)
    length = models.IntegerField()
    available_from = models.DateField()

    def save(self, *args, **kwargs):
        self.imdb_link = "https://www.imdb.com/title/" + self.imdb_id + "/"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("available_from",)


class Cinema(models.Model):
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="cinema_logo/", blank=True, null=True)

    def __str__(self):
        return " - ".join((self.name, self.city))


class Hall(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name="halls")
    description = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=50, default="Hall")
    rows = models.IntegerField(default=15)
    seats_per_row = models.IntegerField(default=20)

    def __str__(self):
        return " - ".join((self.name, str(self.cinema)))


class Seat(models.Model):
    hall = models.ForeignKey(
        Hall, on_delete=models.CASCADE, related_name="seats", null=True
    )
    name = models.CharField(max_length=4, default="A1")
    occupied = models.BooleanField(default=False)

    def __str__(self):
        return format_html(f"Seat: {self.name}<br>Hall: {str(self.hall)}")


class PlayingTime(models.Model):
    assigned_movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="playing_times"
    )
    assigned_hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def add_time(self):
        time = datetime(
            year=self.start_time.year,
            month=self.start_time.month,
            day=self.start_time.day,
            hour=self.start_time.hour,
            minute=self.start_time.minute,
            second=self.start_time.second,
        )
        return time + timedelta(minutes=self.assigned_movie.length)

    def save(self, *args, **kwargs):
        self.end_time = self.add_time()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return format_html(
            f"{self.assigned_movie.name}<br> Start time: {self.start_time.hour}:{self.start_time.minute}"
        )


class Reservation(models.Model):
    seat = models.OneToOneField(Seat, on_delete=models.CASCADE)
    reservation_name = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    reserved_time = models.ForeignKey(
        PlayingTime, on_delete=models.CASCADE, related_name="reservations"
    )
    confirmed = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)

    def __str__(self):
        return format_html(
            f"Name: {str(self.reservation_name)}<br> {str(self.seat)}<br>Movie: {self.reserved_time.assigned_movie}"
        )


def generate_seats(rows, seats_per_row):
    seats = []
    for row in range(0, rows):
        for seat_letter in range(1, seats_per_row + 1):
            seat = Seat(name=str(seat_letter) + (chr(65 + row)))
            seats.append(seat)
    return seats
