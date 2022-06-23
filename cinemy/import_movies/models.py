from django.db import models
from import_movies.utils import validate_file_extension


class ImportMoviesModel(models.Model):
    file = models.FileField(
        upload_to="imported_zips/", validators=[validate_file_extension]
    )
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title
