from django.db import migrations
from datetime import datetime
from datetime import timedelta
import random


def combine_names(apps, schema_editor):
    Cinema = apps.get_model('reservations', 'Cinema')
    Room = apps.get_model('reservations', 'Room')
    Movie = apps.get_model('reservations', 'Movie')
    Projection = apps.get_model('reservations', 'Projection')
    ReservationSelected = apps.get_model('reservations', 'ReservationSelected')
    ReservationFinished = apps.get_model('reservations', 'ReservationFinished')

    default_rows_columns = 20
    cinemas_num = 10
    rooms_per_cinema = 5
    movies_list = get_star_wars_movies()
    projections_start_date = datetime.now()
    projections_start_date = projections_start_date + + timedelta(days=20)
    projections_start_date = projections_start_date.replace(hour=1, minute=00)
    projections_period = 10

    for cinema_idx in range(cinemas_num):
        cinema = Cinema()
        cinema.name = f"Cinema {cinema_idx}"
        cinema.save()

    for cine in Cinema.objects.all():
        for room_idx in range(rooms_per_cinema):
            room = Room()
            room.number = room_idx
            room.cinema = cine
            room.prices = get_random_prices(default_rows_columns * default_rows_columns)
            room.save()

    for _, mov in movies_list.items():
        movie = Movie()
        movie.name = mov['title']
        movie.year = mov['release_year']
        movie.save()

    movies_list = Movie.objects.all()

    #  For each Cinema Room we create 2 projections each day
    for room in Room.objects.all():
        for day_idx in range(projections_period):
            proj_date = projections_start_date + timedelta(days=day_idx)
            proj_date_1 = proj_date.replace(hour=random.randint(12, 15), minute=00, second=00)
            proj_date_2 = proj_date.replace(hour=random.randint(19, 22), minute=00, second=00)

            movie = get_random_movie(movies_list)
            create_projection(Projection, movie, room, proj_date_1, proj_date_1, 3)

            movie = get_random_movie(movies_list)
            create_projection(Projection, movie, room, proj_date_2, proj_date_2, 3)



    #states
    reservation_selected = ReservationSelected()
    reservation_selected.name = 'selected';
    reservation_selected.save()
    reservation_finished = ReservationFinished()
    reservation_finished.name = 'finished';
    reservation_finished.save()


def get_random_prices(amount):
    return ','.join([str(random.randint(1, 100)) for _ in range(amount)])


def create_projection(projection, movie, room, date, start, end_delta):
    projection = projection()
    projection.movie = movie
    projection.room = room
    projection.date = date
    projection.start_time = start
    projection.end_time = start + timedelta(hours=end_delta)
    projection.save()


class Migration(migrations.Migration):
    dependencies = [
        ('reservations', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(combine_names),
    ]


#  Helpers
def get_random_movie(movies_list):
    return random.choice(movies_list)


def get_star_wars_movies():
    movies_list = get_movies_list()
    return movies_list['Star Wars']


def get_movies_list():
    return {
        "Star Wars": {
            "Episode I: The Phantom Menace": {
                "movie_id": 1,
                "title": "Episode I: The Phantom Menace",
                "category_name": "Science Fiction",
                "release_year": 1999
            },
            "Episode II: Attack of the Clones": {
                "movie_id": 2,
                "title": "Episode II: Attack of the Clones",
                "release_year": 2002
            },
            "Episode III: Revenge of the Sith": {
                "movie_id": 3,
                "title": "Episode III: Revenge of the Sith",
                "release_year": 2005
            },
            "Episode IV: A New Hope": {
                "movie_id": 4,
                "title": "Episode IV: A New Hope",
                "release_year": 1977
            },
            "Episode V: The Empire Strikes Back": {
                "movie_id": 5,
                "title": "Episode V: The Empire Strikes Back",
                "release_year": 1980
            },
            "Episode VI: Return of the Jedi": {
                "movie_id": 6,
                "title": "Episode VI: Return of the Jedi",
                "release_year": 1983
            },
            "Episode VII: The Force Awakens": {
                "movie_id": 7,
                "title": "Episode VII: The Force Awakens",
                "release_year": 2015
            },
            "Rogue One: A Star Wars Story": {
                "movie_id": 8,
                "title": "Rogue One: A Star Wars Story",
                "release_year": 2016
            },
            "Episode VIII: The Last Jedi": {
                "movie_id": 9,
                "title": "Star Wars: The Last Jedi",
                "release_year": 2017
            },
            "Solo: A Star Wars Story": {
                "movie_id": 10,
                "title": "Solo: A Star Wars Story",
                "release_year": 2018
            }
        }
    }
