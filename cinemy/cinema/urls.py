from django.urls import path
from cinema.views import select_cinema

urlpatterns = [
    path("select_cinema/", select_cinema, name="select_cinema"),
]
