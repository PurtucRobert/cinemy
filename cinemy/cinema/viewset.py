from rest_framework import viewsets
from cinema.models import Movie
from cinema.serializers import MovieSerializer
from cinema.models import PlayingTime
from cinema.utils import get_current_week_as_range


class MovieCurrentlyPlayingViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Movie.objects.filter(
        pk__in=PlayingTime.objects.filter(
            start_time__range=get_current_week_as_range()
        ).values_list("assigned_movie", flat=True)
    )
    serializer_class = MovieSerializer
