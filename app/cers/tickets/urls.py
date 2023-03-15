from cers.tickets import views
from django.urls import path

app_name = 'tickets'

urlpatterns = [
    path('accept_ticket/', views.accept_ticket),
]
