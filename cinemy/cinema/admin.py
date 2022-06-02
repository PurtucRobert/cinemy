from django.contrib import admin
from cinema.models import Movie, Cinema, Hall


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    exclude = ("imdb_link",)


class HallInline(admin.TabularInline):
    model = Hall
    extra = 0


@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    inlines = (HallInline,)


admin.site.register(Hall)
