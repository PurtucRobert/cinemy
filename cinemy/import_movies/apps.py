from django.apps import AppConfig


class ImportMoviesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "import_movies"

    def ready(self):

        from import_movies.signals import handlers
