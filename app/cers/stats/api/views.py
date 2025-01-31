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
    month = datetime.today().month
    year = datetime.today().year
    technicians_list = CersUser.objects.filter(groups__name='technician')
    data = [{'id': technician.id, 'technician': technician.username,
             'tickets': technician.tasks.filter(closed_date=datetime.today()).count(),
             'tickets_current_month': technician.tasks.filter(closed_date__month=month,
                                                              closed_date__year=year).count(),
             'time': sum(technician.tasks.filter(closed_date=datetime.today()).values_list("duration",
                                                                                           flat=True)),
             'time_current_month': sum(technician.tasks.filter(closed_date__month=month,
                                                               closed_date__year=year).values_list("duration",
                                                                                                   flat=True))
             } for
            technician in technicians_list]
    return Response({'data': data}, status=status.HTTP_200_OK)

@api_view(['GET'])
def technicians_tickets_year(request, year):
    technicians_list = CersUser.objects.filter(groups__name='technician')
    data = [{'label': technician.username,
             'data': [technician.tasks.filter(closed_date__month=m, closed_date__year=year).count() for m in
                      range(1, 13)],
             'backgroundColor': technician.color} for technician in technicians_list]
    return Response({'data': {'data': data}}, status=status.HTTP_200_OK)
