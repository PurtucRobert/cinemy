from django.db.models.signals import post_save
from django.dispatch import receiver
from import_movies.utils import import_movies_from_uploaded_zip
from import_movies.models import ImportMoviesModel


@receiver(post_save, sender=ImportMoviesModel)
def process_zip_file(instance, **kwargs):
    import_movies_from_uploaded_zip(instance.title, instance.file)
