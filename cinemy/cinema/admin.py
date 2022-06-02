from django.contrib import admin
from cinema.models import Movie, Cinema, Hall


class MovieAdmin(admin.ModelAdmin):
    exclude = ("imdb_link",)


admin.site.register(Movie, MovieAdmin)
admin.site.register(Cinema)
admin.site.register(Hall)
