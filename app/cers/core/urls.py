from cers.core import views
from django.urls import path

app_name = 'core'

urlpatterns = [
    path('set_subsidiary_context/', views.set_subsidiary_context, name='set_subsidiary_context'),
]
