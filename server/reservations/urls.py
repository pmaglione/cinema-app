from django.conf.urls import url
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'reservations'
urlpatterns = [
    url(r"^get/(?P<pk>\d*)/$", views.Projections.get_projection),
    url(r'^all$', views.Projections.get_all),
    url(r"^update/(?P<pk>\d*)/$", views.Projections.update),
    url(r"^get_by_username/(?P<username>\w*)/$", views.Reservations.get_by_username),
    url(r"^checkout/(?P<reservation_id>\d*)/$", csrf_exempt(views.Reservations.checkout)),
    url(r"^cancel/(?P<reservation_id>\d*)/$", csrf_exempt(views.Reservations.cancel))
]
