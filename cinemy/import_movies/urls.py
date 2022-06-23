from django.urls import path
from import_movies.views import import_movies

urlpatterns = [path("", import_movies, name="import_movies")]
