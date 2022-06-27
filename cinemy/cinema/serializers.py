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
        fields = "__all__"


class PlayingTimeForDetailedMovieSerializer(serializers.ModelSerializer):
    assigned_hall = HallSerializer()

    class Meta:
        model = PlayingTime
        exclude = (
            "id",
            "assigned_movie",
        )


class PlayingTimeSerializer(serializers.ModelSerializer):
    hall = HallSerializer(source="assigned_hall")
    movie = MovieSerializer(source="assigned_movie")

    class Meta:
        model = PlayingTime
        exclude = ("id",)


class DetailedMovieSerializer(serializers.ModelSerializer):
    playing_times = PlayingTimeForDetailedMovieSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        exclude = ("id",)
