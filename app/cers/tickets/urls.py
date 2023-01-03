from django.urls import path

from cers.tickets import views

app_name = 'tickets'

urlpatterns = [
    path('accept_ticket/', views.accept_ticket),

]
