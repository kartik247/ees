from django.urls import path
from . import views

urlpatterns = [
    path('institutes/', views.institute_list),
    path('generateConfig/<int:pkid>/', views.institute_detail),
    path('fetchConfigFile/<str:filename>/', views.fetchConfigFile),
]
