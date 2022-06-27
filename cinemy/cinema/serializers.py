from rest_framework import serializers
from cinema.models import Movie, PlayingTime, Hall, Cinema


class CinemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cinema
        exclude = ("id",)


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        exclude = ("id",)


class HallSerializer(serializers.ModelSerializer):
    cinema = CinemaSerializer()

    class Meta:
        model = Hall
        exclude = ("id",)


class PlayingTimeForDetailedMovieSerializer(serializers.ModelSerializer):
    assigned_hall = HallSerializer()

    class Meta:
        model = PlayingTime
        exclude = (
            "id",
            "assigned_movie",
        )


class DetailedMovieSerializer(serializers.ModelSerializer):
    playing_times = PlayingTimeForDetailedMovieSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        exclude = ("id",)
