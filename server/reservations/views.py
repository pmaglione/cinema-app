from rest_framework import viewsets
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from reservations.models import Projection, Reservation, ReservationFinished
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from reservations.serializers import ProjectionSerializer, UserSerializer, ReservationSerializer
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework import generics
from django.contrib.auth.models import User
import random
import json


class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)


class Projections(APIView):
    def get_all(request):
        projections = Projection.objects.all()

        serializer = ProjectionSerializer(projections, many=True)

        return JsonResponse(serializer.data, safe=False)

    def get_projection(request, pk):
        projection = Projection.objects.get(pk=pk)

        serializer = ProjectionSerializer(projection, many=False)
        return JsonResponse(serializer.data, safe=False)

    def update(request, pk):
        projection = Projection.objects.get(pk=pk)
        rand = random.randint(1,10)
        projection.reserved_seats = str(rand)
        projection.save()

        return JsonResponse(json.dumps({}), safe=False)


class ProjectionViewSet(viewsets.ViewSet):
    """
    API endpoint for projection
    """

    def get(self, request):
        queryset = Projection.objects.get(pk=self.request.projection_id)
        serializer = ProjectionSerializer(queryset, many=False, context={'request': request})
        return JsonResponse(serializer.data)


class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Reservations(APIView):
    def get_by_username(self, username):
        user = User.objects.get(username=username)
        reservations = Reservation.objects.filter(author=user.id)

        serializer = ReservationSerializer(reservations, many=True)

        return JsonResponse(serializer.data, safe=False)

    def checkout(self, reservation_id):
        reservation = Reservation.objects.get(pk=reservation_id)
        reservation.state = ReservationFinished.objects.first()
        reservation.save()

        return JsonResponse({}, safe=False)

    def cancel(self, reservation_id):
        reservation = Reservation.objects.get(pk=reservation_id)
        seats = reservation.seats.split(',')
        projection = Projection.objects.get(pk=reservation.projection.id)
        projection_reserved_seats = projection.get_reserved_seats_list()
        remaining_reserved_seats = [x for x in projection_reserved_seats if x not in seats]
        projection.set_reserved_seats_arr(remaining_reserved_seats)

        reservation.delete()
        projection.save()

        return JsonResponse({'ok': True}, safe=False)


#  emergency methods created because of crsf gcloud prod problem
def login(request):
    body = json.loads(request.body)
    username = body['username']
    password = body['password']
    user = User.objects.get(username=username)

    if user:
        check_password = user.check_password(password)
        print(check_password)
        if check_password:
            return JsonResponse({'ok': True})
        else:
            return JsonResponse({'ok': False}, status=403)
    else:
        return JsonResponse({'ok': False}, status=403)


def logout(request):
    return JsonResponse({'ok': True})


def registration(request):
    body = json.loads(request.body)
    username = body['username']
    email = body['email']
    password1 = body['password1']
    password2 = body['password2']

    if username != "" and email != "" and password1 != "" and password1 == password2:
        user = User(username=username, email=email)
        user.set_password(password1)
        user.save()

        return JsonResponse({'ok': True})
    else:
        return JsonResponse({'ok': False}, status=403)

