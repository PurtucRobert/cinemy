from rest_framework import response, status
from rest_framework import serializers
from cinema.models import Movie, PlayingTime, Hall, Cinema


class CinemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cinema
        exclude = ("id",)


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"


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
        fields = ("hall", "movie", "start_time", "id")


class PlayingTimeCreateSerializer(serializers.Serializer):
    hall = serializers.IntegerField()
    movie = serializers.IntegerField()
    start_time = serializers.DateTimeField()

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def create(self, validated_data):
        instance = PlayingTime.objects.create(
            assigned_movie_id=validated_data["movie"],
            assigned_hall_id=validated_data["hall"],
            start_time=validated_data["start_time"],
        )
        return instance


class DetailedMovieSerializer(serializers.ModelSerializer):
    playing_times = PlayingTimeForDetailedMovieSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        exclude = ("id",)
