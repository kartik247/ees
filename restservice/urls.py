from django.urls import path
from . import views

urlpatterns = [
    path('feedData/', views.institute_list),
    path('generateConfig/<int:pkid>/', views.institute_detail),
]
