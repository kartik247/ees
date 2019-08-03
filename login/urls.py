from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.display, name='display'),
    #url(r'^assignments/', views.assignments, name='assignments'),
    #url(r'^insertassignment/', views.insertassignment, name='insertassignment'),
    #url(r'^getassignmentdetails/', views.getassignmentdetails, name='getassignmentdetails'),
    #url(r'^resetpod/', views.resetpod, name='resetpod'),
]