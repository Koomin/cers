from django.urls import path

from cers.core import views

app_name = 'core'

urlpatterns = [
    path('set_subsidiary_context/', views.set_subsidiary_context, name='set_subsidiary_context'),
]
