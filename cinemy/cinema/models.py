from django.db import models

# Create your models here.
SEATS = (
    (1, "A1"),
    (2, "A2"),
    (3, "A3"),
    (4, "A4"),
    (5, "A5"),
    (6, "B1"),
    (7, "B2"),
    (8, "B3"),
    (9, "B4"),
    (10, "B5"),
    (11, "C1"),
    (12, "C2"),
    (13, "C3"),
    (14, "C4"),
    (15, "C5"),
)


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
        return self.name


class Hall(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=50, default="Hall")

    def __str__(self):
        return self.name


class Seat(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    name = models.IntegerField(choices=SEATS, default=1)
