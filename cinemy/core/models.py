from django.db import models

# Create your models here.


class Movie(models.Model):
    name = models.CharField(max_length=100)
    poster = models.ImageField(upload_to="posters/", blank=True, null=True)
    description = models.TextField()
    imdb_link = models.CharField(max_length=100)
    imdb_id = models.CharField(max_length=100)
    trailer_url = models.CharField(max_length=100)
    length = models.TimeField()
    available_from = models.DateField()

    @classmethod
    def create(
        cls, name="", poster="", description="", imdb_id="", trailer_url="", length=None
    ):
        movie = cls(
            name=name,
            poster=poster,
            description=description,
            imdb_id=imdb_id,
            imdb_link="https://www.imdb.com/title/" + imdb_id + "/",
            trailer_url=trailer_url,
            length=length,
        )
        return movie

    class Meta:
        ordering = ("available_from",)
