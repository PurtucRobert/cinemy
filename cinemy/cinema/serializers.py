from requests import request
from rest_framework import serializers
from cinema.models import Movie, PlayingTime, Hall, Cinema, Reservation
from django.contrib.auth.models import User


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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


class ReservationSerializer(serializers.ModelSerializer):
    reserved_time = PlayingTimeSerializer(read_only=True)
    reservation_name = UserSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = "__all__"


class ReservationCreateSerializer(serializers.Serializer):
    seat = serializers.IntegerField()
    reservation_name = serializers.CharField()
    reserved_time = serializers.IntegerField()
    confirmed = serializers.BooleanField()
    expired = serializers.BooleanField()

    def validate_reservation_name(self, data):
        try:
            user = User.objects.get(username=data)
            request_user = self.context["request"].user
            if (user != request_user) and not request_user.is_superuser:
                raise serializers.ValidationError(
                    f"Payload username is not matching token"
                )
        except User.DoesNotExist:
            raise serializers.ValidationError(f"Username: {data} does not exists")
        return data

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def create(self, validated_data):
        instance = Reservation.objects.create(
            seat_id=validated_data["seat"],
            reservation_name=User.objects.get(
                username=validated_data["reservation_name"]
            ),
            reserved_time_id=validated_data["reserved_time"],
        )
        return instance
