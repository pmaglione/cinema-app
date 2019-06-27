from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/projection/(?P<projection_id>[^/]+)/$', consumers.ProjectionConsumer),
]