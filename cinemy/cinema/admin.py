from django.contrib import admin
from cinema.models import Movie, Cinema, Hall, Seat
from nested_inline.admin import NestedTabularInline, NestedModelAdmin


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    exclude = ("imdb_link",)


class SeatInline(NestedTabularInline):
    model = Seat
    extra = 0


class HallInline(NestedTabularInline):
    model = Hall
    extra = 0
    inlines = (SeatInline,)


@admin.register(Cinema)
class CinemaAdmin(NestedModelAdmin):
    inlines = (HallInline,)


@admin.register(Hall)
class HallAdmin(NestedModelAdmin):
    inlines = (SeatInline,)


admin.site.register(Seat)
