from django.urls import path

from . import views

urlpatterns = [
    path('', views.driver_site, name='driver_site'),
    path('get_drivers/', views.get_drivers, name='get_drivers'),
]
