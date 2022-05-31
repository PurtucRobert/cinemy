from django.db import models
import datetime

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

    class Meta:
        ordering = ("available_from",)
