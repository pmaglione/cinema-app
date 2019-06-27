from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView, RedirectView
from reservations import views
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('reservations/', include('reservations.urls')),
    path(r'', RedirectView.as_view(url='/reservations/'), name='login-redirect'),
    path('users', views.UserListView.as_view()),
    path('rest-auth/login/', views.login),
    path('rest-auth/logout/', views.logout),
    path('rest-auth/registration/', views.registration),
]
