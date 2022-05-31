from django.contrib import admin
from core.models import Movie


class MovieAdmin(admin.ModelAdmin):
    exclude = ("imdb_link",)


admin.site.register(Movie, MovieAdmin)
# Register your models here.
