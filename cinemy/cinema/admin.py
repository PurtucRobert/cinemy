from django.contrib import admin
from cinema.models import Movie, Cinema, Hall, Seat, Reservation, PlayingTime
from nested_inline.admin import NestedTabularInline, NestedModelAdmin


class ReservationInline(NestedTabularInline):
    model = Reservation


class SeatInline(NestedTabularInline):
    model = Seat
    extra = 0
    inlines = (ReservationInline,)


class HallInline(NestedTabularInline):
    model = Hall
    extra = 0
    inlines = (SeatInline,)


class PlayingTimeInline(NestedTabularInline):
    model = PlayingTime


@admin.register(Cinema)
class CinemaAdmin(NestedModelAdmin):
    inlines = (HallInline,)


@admin.register(Hall)
class HallAdmin(NestedModelAdmin):
    inlines = (SeatInline,)


@admin.register(Reservation)
class ReservationAdmin(NestedModelAdmin):
    exclude = ("is_reserved",)


@admin.register(Movie)
class MovieAdmin(NestedModelAdmin):
    inlines = (PlayingTimeInline,)
    exclude = ("imdb_link",)


@admin.register(PlayingTime)
class PlayingTime(NestedModelAdmin):
    readonly_fields = ("end_time",)
    exclude = ("end_time",)


admin.site.register(Seat)
