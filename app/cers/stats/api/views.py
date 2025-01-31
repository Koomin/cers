from datetime import datetime

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from cers.cers_auth.models import CersUser
from cers.companies.models import Company


@api_view(['GET'])
def companies(request):
    companies_count = Company.objects.all().count()
    companies_tickets_sum = [
        {'company': company.name, 'id': company.id, 'tickets': company.ticket_set.all().count()} for company in
        Company.objects.all()]
    data = {
        'companies_count': companies_count,
        'companies_tickets': companies_tickets_sum,
    }
    return Response({'data': data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def companies_year(request, year):
    data = [{'label': company.name,
             'data': [company.ticket_set.filter(created__year=year, created__month=m).count() for m in range(1, 13)],
             'backgroundColor': company.color} for company in Company.objects.all()]
    return Response({'data': data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def technicians(request):
    technicians_list = CersUser.objects.filter(groups__name='technicians')
    data = [{'id': technician.id, 'tickets': technician.tasks.filter(closed_date=datetime.today()),
             'time': sum(technician.tasks.filter(closed_date=datetime.today()).values_list("duration", flat=True))} for
            technician in technicians_list]
    return Response({'data': data}, status=status.HTTP_200_OK)

@api_view(['GET'])
def technicians_tickets_year(request, year):
    technicians_list = CersUser.objects.filter(groups__name='technicians')
    data = [{'label': "",
             'data': [technician.tasks.filter(closed_date__month=m, closed_date__year=year).count() for m in
                      range(1, 13)],
             'backgroundColor': ""} for technician in technicians_list]
    return Response({'data': {'data': data}}, status=status.HTTP_200_OK)
