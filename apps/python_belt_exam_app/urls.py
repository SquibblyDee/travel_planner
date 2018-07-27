from django.conf.urls import url
from . import views

urlpatterns = [
    # root goes to the index
    url(r'^$', views.loginandreg),
    url(r'^process_register$', views.process_register),
    url(r'^process_login$', views.process_login),
    url(r'^travels$', views.landing),
    url(r'^addtrip$', views.addtrip),
    url(r'^back$', views.back),
    url(r'^process_trip$', views.processtrip),
    url(r'^view/(?P<trip_id>\d+)$', views.show_process),
    url(r'^join/(?P<trip_id>\d+)$', views.join_process),
    url(r'^cancel/(?P<trip_id>\d+)$', views.cancel_process),
    url(r'^delete/(?P<trip_id>\d+)$', views.delete_process),
    url(r'^logout$', views.logout),
]
