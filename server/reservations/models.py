from django.core.validators import validate_comma_separated_integer_list
from django.db import models
from django.contrib.auth.models import User
import datetime


DEFAULT_ROWS_COLUMNS = 20
RESERVATION_STATE_SELECTED = 'selected'
RESERVATION_STATE_FINISHED = 'finished'


class Cinema(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    number = models.IntegerField(default=0)
    cinema = models.ForeignKey(Cinema, on_delete=models.PROTECT)
    num_columns = models.IntegerField(default=DEFAULT_ROWS_COLUMNS)
    num_rows = models.IntegerField(default=DEFAULT_ROWS_COLUMNS)
    prices = models.TextField(validators=[validate_comma_separated_integer_list])

    def get_seats_amount(self):
        return self.num_columns * self.num_rows

    def get_seats_list(self):
        return list(range(self.get_seats_amount()))

    def __str__(self):
        return f"Room {self.number} of {self.cinema}"


class Movie(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.name} of year {self.year}"


class Projection(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT)
    room = models.ForeignKey(Room, on_delete=models.PROTECT)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    reserved_seats = models.TextField(validators=[validate_comma_separated_integer_list])

    def __str__(self):
        return f"{self.movie} in {self.room} at {self.date.strftime('%d/%m/%Y')} - {self.start_time.strftime('%H:%M')}"

    def get_duration(self):
        dateTimeA = datetime.datetime.combine(datetime.date.today(), self.start_time)
        dateTimeB = datetime.datetime.combine(datetime.date.today(), self.end_time)
        return (dateTimeA - dateTimeB).total_seconds() / 3600

    def add_seats_reservation(self, new_seats_list):
        reserved_seats_list = self.reserved_seats.split(",")
        new_seats = new_seats_list.split(",")
        reserved_seats_list += new_seats

        self.reserved_seats = ','.join(reserved_seats_list)

    def set_reserved_seats_arr(self, seats_arr):
        self.reserved_seats = ','.join(seats_arr)

    def get_reserved_seats_list(self):
        return self.reserved_seats.split(",")

    def get_free_seats(self):
        return [seat_id for seat_id in self.room.get_seats_list() if seat_id not in self.get_reserved_seats_list()]


class ReservationState(models.Model):
    name = models.CharField(max_length=50)

    def finish(self, reservation):
        raise Exception("This method should not be called in this state")

    def cancel(self, reservation):
        reservation.state = ReservationCanceled()


class ReservationSelected(ReservationState):
    def select(self, reservation):
        pass

    def finish(self, reservation):
        reservation.state = ReservationFinished()

    ReservationState._meta.get_field('name').default = RESERVATION_STATE_SELECTED


class ReservationFinished(ReservationState):
    ReservationState._meta.get_field('name').default = RESERVATION_STATE_FINISHED


class ReservationCanceled(ReservationState):
    def cancel(self, reservation):
        raise Exception("This method should not be called in this state")


class Reservation(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    state = models.ForeignKey(ReservationState, on_delete=models.PROTECT)
    projection = models.ForeignKey(Projection, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    seats = models.TextField(validators=[validate_comma_separated_integer_list])

    def get_seats_amount(self):
        return len(self.seats.split(','))

    def __str__(self):
        return f"{self.author} reserved {self.year} seats for {self.projection}"
