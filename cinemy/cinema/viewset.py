from rest_framework import viewsets
from cinema.serializers import (
    MovieSerializer,
    DetailedMovieSerializer,
    PlayingTimeSerializer,
    PlayingTimeCreateSerializer,
    HallSerializer,
    ReservationSerializer,
    ReservationCreateSerializer,
)
from cinema.models import PlayingTime, Hall, Movie, Reservation
from cinema.utils import get_current_week_as_range
from django_filters import rest_framework as filters
from login.permissions import IsOwner
from login.authentication import BearerAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import response, status


class CustomerAuthMixin:
    authentication_classes = [BearerAuthentication]
    permission_classes = [IsAuthenticated]


class AdminAuthMixin:
    authentication_classes = [BearerAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]


class IsOwnerAuthMixin:
    authentication_classes = [BearerAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]


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


class PlayingTimeViewSet(AdminAuthMixin, viewsets.ModelViewSet):
    queryset = PlayingTime.objects.all()
    serializer_classes = {
        "list": PlayingTimeSerializer,
        "retrieve": PlayingTimeSerializer,
        "create": PlayingTimeCreateSerializer,
    }
    default_serializer_class = PlayingTimeSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        instance_serializer = PlayingTimeSerializer(instance)
        return response.Response(
            instance_serializer.data, status=status.HTTP_201_CREATED
        )


class UserReservationViewSet(IsOwnerAuthMixin, viewsets.ModelViewSet):
    serializer_classes = {
        "list": ReservationSerializer,
        "retrieve": ReservationSerializer,
        "create": ReservationCreateSerializer,
    }
    default_serializer_class = ReservationSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Reservation.objects.all()
        return Reservation.objects.filter(reservation_name=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        instance_serializer = self.default_serializer_class(instance)
        return response.Response(
            instance_serializer.data, status=status.HTTP_201_CREATED
        )
