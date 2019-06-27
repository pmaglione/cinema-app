from rest_framework import serializers, fields
from reservations.models import Projection, Room, Cinema, Movie, ReservationState, Reservation
from django.contrib.auth.models import User


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'


class CinemaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cinema
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    cinema = CinemaSerializer(many=False, read_only=True)

    class Meta:
        model = Room
        fields = '__all__'


class ProjectionSerializer(serializers.ModelSerializer):
    date = fields.DateField(format='%d/%m/%Y')
    start_time = fields.DateField(format='%H:%M')
    end_time = fields.DateField(format='%H:%M')
    room = RoomSerializer(many=False, read_only=True)
    movie = MovieSerializer(many=False, read_only=True)

    class Meta:
        model = Projection
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', )


class ReservationStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationState
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False, read_only=True)
    state = ReservationStateSerializer(many=False, read_only=True)
    projection = ProjectionSerializer(many=False, read_only=True)
    created_date = fields.DateTimeField(format='%d/%m/%Y %H:%M')

    class Meta:
        model = Reservation
        fields = '__all__'
