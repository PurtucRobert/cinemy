from django.urls import include, path
from cinema.views import (
    select_cinema,
    select_movie,
    select_timeframe,
    select_seats,
    MovieDetail,
    reservations_per_user,
    confirm_reservations,
)
from rest_framework.routers import DefaultRouter
from cinema.viewset import MovieCurrentlyPlayingViewSet

router = DefaultRouter()
router.register(
    "movies_playing_this_week",
    MovieCurrentlyPlayingViewSet,
    basename="movies_playing_this_week",
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
    path("reservations/<pk>", reservations_per_user, name="reservations_per_user"),
    path(
        "confirm_reservation/<slug:uidb64>/",
        confirm_reservations,
        name="confirm_reservations",
    ),
    path("api/", include(router.urls)),
]
