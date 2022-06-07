from django.urls import path
from cinema.views import select_cinema, select_movie, select_timeframe, select_seats

urlpatterns = [
    path("select_cinema/", select_cinema, name="select_cinema"),
    path("select_movie/<int:cinema_id>", select_movie, name="select_movie"),
    path(
        "select_timeframe/<int:movie_id>/<int:cinema_id>/",
        select_timeframe,
        name="select_timeframe",
    ),
    path("select_seats/<pk>", select_seats, name="select_seats"),
]
