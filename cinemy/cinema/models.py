from django.db import models

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


class Seat(models.Model):
    pass


class Cinema(models.Model):
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Hall(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
