from django.db import models
from django.utils.html import format_html

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

    def __str__(self):
        return " - ".join((self.name, self.city))


class Hall(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=50, default="Hall")
    rows = models.IntegerField(default=15)
    seats_per_row = models.IntegerField(default=20)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for row in range(0, self.rows):
            for seat in range(1, self.seats_per_row + 1):
                seat = Seat(hall=self, name=(chr(65 + row) + str(seat)))
                seat.save()

    def __str__(self):
        return " - ".join((self.name, str(self.cinema)))


class Seat(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    name = models.CharField(max_length=4, default="A1")
    is_reserved = models.BooleanField(default=False)

    def __str__(self):
        return format_html(f"Seat: {self.name}<br>Hall: {str(self.hall)}")
