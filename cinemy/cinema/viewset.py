from rest_framework import viewsets
from cinema.serializers import (
    MovieSerializer,
    DetailedMovieSerializer,
    PlayingTimeSerializer,
    HallSerializer,
)
from cinema.models import PlayingTime, Hall, Movie
from cinema.utils import get_current_week_as_range
from django_filters import rest_framework as filters
from login.authentication import BearerAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class CustomerAuthMixin:
    authentication_classes = [BearerAuthentication]
    permission_classes = [IsAuthenticated]


class AdminAuthMixin:
    authentication_classes = [BearerAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]


class MovieCurrentlyPlayingViewSet(CustomerAuthMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Movie.objects.filter(
        pk__in=PlayingTime.objects.filter(
            start_time__range=get_current_week_as_range()
        ).values_list("assigned_movie", flat=True)
    )
    serializer_class = MovieSerializer


class MovieCurrentlyPlayingDetailedViewSet(
    CustomerAuthMixin, viewsets.ReadOnlyModelViewSet
):
    serializer_class = DetailedMovieSerializer


class PlayingTimeFilter(filters.FilterSet):
    class Meta:
        model = PlayingTime
        fields = ["assigned_movie__imdb_id", "assigned_movie__name"]


class SearchMovieViewSet(CustomerAuthMixin, viewsets.ReadOnlyModelViewSet):
    queryset = PlayingTime.objects.all()
    serializer_class = PlayingTimeSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = PlayingTimeFilter


class HallViewSet(AdminAuthMixin, viewsets.ModelViewSet):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [BearerAuthentication]


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = [BearerAuthentication]

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
