from django.urls import path
from cinema.views import (
    select_cinema,
    select_movie,
    select_timeframe,
    select_seats,
    MovieDetail,
)

urlpatterns = [
    path("book_a_ticket/select_cinema/", select_cinema, name="select_cinema"),
    path(
        "book_a_ticket/select_movie/<int:cinema_id>", select_movie, name="select_movie"
    ),
    path(
        "book_a_ticket/select_timeframe/<int:movie_id>/<int:cinema_id>/",
        select_timeframe,
        name="select_timeframe",
    ),
    path("book_a_ticket/select_seats/<pk>", select_seats, name="select_seats"),
    path("movie_detail/<pk>", MovieDetail.as_view(), name="movie_detail"),
]
