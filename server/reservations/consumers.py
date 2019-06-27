from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from .models import Projection, Reservation, ReservationSelected, ReservationFinished
from django.contrib.auth.models import User
from background_task import background


class ProjectionConsumer(WebsocketConsumer):
        def connect(self):
            self.projection_id = self.scope['url_route']['kwargs']['projection_id']
            self.projection_group_name = 'projection_%s' % self.projection_id

            self.check_expiration(repeat=120, repeat_until=None)

            async_to_sync(self.channel_layer.group_add)(
                self.projection_group_name,
                self.channel_name
            )

            self.accept()

        def disconnect(self, close_code):
            async_to_sync(self.channel_layer.group_discard)(
                self.projection_group_name,
                self.channel_name
            )

        # Receive message from WebSocket
        def receive(self, text_data):
            text_data_json = json.loads(text_data)
            action = text_data_json['action']

            if action == 'book':
                self.manage_book(text_data_json)

        # Receive message from room group
        def reservation_update(self, event):
            data = event['data']

            self.send(json.dumps(data))

        def manage_book(self, text_data_json):
            id = text_data_json['id']
            username = text_data_json['username']
            seats = text_data_json['seats']

            # update projection seats availability
            projection = Projection.objects.get(pk=id)
            actual_seats = projection.reserved_seats.split(',')
            new_seats = seats.split(',')
            total_seats = actual_seats + new_seats
            projection.reserved_seats = ",".join(total_seats)
            projection.save()

            # save book
            reservation = Reservation()
            reservation.author = User.objects.get(username=username)
            reservation.projection = projection
            reservation.state = ReservationSelected.objects.first()
            reservation.seats = seats
            reservation.save()

            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.projection_group_name,
                {
                    'type': 'reservation_update',
                    'data': {
                        'id': projection.id,
                        'reserved_seats': projection.reserved_seats,
                        'username': username
                    }
                }
            )

        @background(schedule=120)
        def check_expiration(self):
            print("Hello World!")
