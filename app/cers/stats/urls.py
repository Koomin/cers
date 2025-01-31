from django.urls import path
from cers.stats.api.views import companies, companies_year, technicians, technicians_tickets_year

urlpatterns = [
    path('companies/', companies, name='companies'),
    path('companies/<int:year>/', companies_year, name='companies_year'),
    path('technicians/', technicians, name='technicians'),
    path('technicians/tickets/<int:year>/', technicians_tickets_year, name='technicians_tickets_year'),
]