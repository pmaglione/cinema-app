from django.test import TestCase
from reservations.models import Movie, Cinema, Room, Projection, Reservation, ReservationSelected
from django.contrib.auth.models import User
import datetime


class MovieTestCase(TestCase):
    def setUp(self):
        Movie.objects.create(name="Test Movie", year=2019)

    def test_create(self):
        movie = Movie.objects.get(name="Test Movie")
        self.assertEqual(movie.name, 'Test Movie')
        self.assertEqual(movie.year, 2019)


class CinemaTestCase(TestCase):
    def setUp(self):
        Cinema.objects.create(name="Test Cinema")

    def test_create(self):
        cinema = Cinema.objects.get(name="Test Cinema")
        self.assertEqual(cinema.name, 'Test Cinema')


class RoomTestCase(TestCase):
    ROOM_ID = 123123

    def setUp(self):
        cinema = Cinema.objects.create(name="Test Cinema")
        Room.objects.create(number=self.ROOM_ID, cinema=cinema, num_columns=20, num_rows=20)

    def test_create(self):
        room = Room.objects.get(number=self.ROOM_ID)
        self.assertEqual(room.number, self.ROOM_ID)
        self.assertEqual(room.get_seats_amount(), 400)
        self.assertEqual(room.cinema.name, "Test Cinema")


class ProjectionTestCase(TestCase):
    projection_id = 0

    def setUp(self):
        movie = Movie.objects.create(name="Test Movie", year=2019)
        cinema = Cinema.objects.create(name="Test Cinema")
        room = Room.objects.create(number=123123, cinema=cinema, num_columns=20, num_rows=20)
        projection = Projection.objects.create(movie=movie, room=room, date=datetime.datetime.now(),
                                  start_time=datetime.datetime.now(), end_time=datetime.datetime.now(),
                                  reserved_seats="1,2,3")
        self.projection_id = projection.id

    def test_create(self):
        projection = Projection.objects.get(pk=self.projection_id)
        self.assertEqual(projection.movie.name, "Test Movie")
        self.assertEqual(projection.reserved_seats, "1,2,3")

    def test_update(self):
        projection = Projection.objects.get(pk=self.projection_id)
        projection.reserved_seats = "1"
        projection.save()
        projection = Projection.objects.get(pk=self.projection_id)
        self.assertEqual(projection.reserved_seats, "1")


class ReservationTestCase(TestCase):
    reservation_id = 0

    def setUp(self):
        movie = Movie.objects.create(name="Test Movie", year=2019)
        cinema = Cinema.objects.create(name="Test Cinema")
        room = Room.objects.create(number=123123, cinema=cinema, num_columns=20, num_rows=20)
        projection = Projection.objects.create(movie=movie, room=room, date=datetime.datetime.now(),
                                               start_time=datetime.datetime.now(), end_time=datetime.datetime.now(),
                                               reserved_seats="1,2,3")
        user = User.objects.create(username='test_user', email='test_user@test_user.com',password='test_user')
        selected = ReservationSelected.objects.create()
        reservation = Reservation.objects.create(author=user, state=selected, projection=projection,
                                                 created_date=datetime.datetime.now(), seats="1,2,3")
        self.reservation_id = reservation.id

    def test_create(self):
        reservation = Reservation.objects.get(pk=self.reservation_id)
        self.assertEqual(reservation.seats, "1,2,3")


