import os
from django.core.exceptions import ValidationError
from zipfile import ZipFile

from django.db import IntegrityError
from cinemy.settings import MEDIA_ROOT
import csv
from pathlib import Path
from django.core.files import File
from cinema.models import Movie


class CsvNotFound(Exception):
    pass


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = [".zip", ".rar"]
    if not ext.lower() in valid_extensions:
        raise ValidationError("Unsupported file extension.")


def extract_zip(zip, path):
    zip_util = ZipFile(zip)
    files = zip_util.namelist()
    for file in files:
        if file.endswith(".csv"):
            zip_util.extractall(path=path)
            return file
    raise CsvNotFound("CSV file was not found in the ZIP file")


def import_movies_from_uploaded_zip(title, zip):
    path = MEDIA_ROOT / "extracted_zips" / title
    csv_file = extract_zip(zip, path)
    with open(path / csv_file) as file:
        csv_reader = csv.DictReader(file, delimiter=";")
        # movies = []
        for movie in csv_reader:
            try:
                poster_path = Path(path / movie["poster"])
                imported_movie = Movie(**movie)
                with poster_path.open(mode="rb") as f:
                    imported_movie.poster = File(f, name=poster_path.name)
                    imported_movie.save()
            except (FileNotFoundError, IntegrityError) as e:
                print(f"Failed to add movie:{movie}, \ne: {e}")
