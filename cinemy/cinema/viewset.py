from rest_framework import viewsets
from cinema.models import Movie
from cinema.serializers import (
    MovieSerializer,
    DetailedMovieSerializer,
    PlayingTimeSerializer,
)
from cinema.models import PlayingTime
from cinema.utils import get_current_week_as_range
from django_filters import rest_framework as filters
from login.authentication import BearerAuthentication
from rest_framework.permissions import IsAuthenticated


class MovieCurrentlyPlayingViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [BearerAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Movie.objects.filter(
        pk__in=PlayingTime.objects.filter(
            start_time__range=get_current_week_as_range()
        ).values_list("assigned_movie", flat=True)
    )
    serializer_class = MovieSerializer


class MovieCurrentlyPlayingDetailedViewSet(MovieCurrentlyPlayingViewSet):
    serializer_class = DetailedMovieSerializer


class PlayingTimeFilter(filters.FilterSet):
    class Meta:
        model = PlayingTime
        fields = ["assigned_movie__imdb_id", "assigned_movie__name"]


class SearchMovieViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PlayingTime.objects.all()
    serializer_class = PlayingTimeSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = PlayingTimeFilter
