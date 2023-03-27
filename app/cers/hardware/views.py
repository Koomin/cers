from cers.companies.models import CompanyConfig
from cers.hardware.models import ComputerSet
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _


def driver_site(request):
    logo = CompanyConfig.objects.get(main_company=True).logo.url
    return render(request, 'custom/drivers.html', {'logo': logo})


def get_drivers(request):
    if request.method == 'GET':
        serial_number = request.GET.get('serial_number')
        try:
            computer_set = ComputerSet.objects.get(serial_number=serial_number)
        except ComputerSet.DoesNotExist:
            response = JsonResponse({})
            response.status_code = 404
            return response
        else:
            data = {
                'computer_model': {'model': computer_set.model.name, 'title': _('Computer model'), 'url': '-'},
                'operating_system': {
                    'model': computer_set.operating_system.name,
                    'title': _('Operating system'),
                    'url': '-',
                },
                'motherboard': {
                    'model': computer_set.motherboard.__str__(),
                    'title': _('Motherboard'),
                    'url': computer_set.motherboard.driver_url or '-',
                },
                'power_supply': {
                    'model': computer_set.power_supply.__str__(),
                    'title': _('Power supply'),
                    'url': computer_set.power_supply.driver_url or '-',
                },
                'processor': {
                    'model': computer_set.processor.__str__(),
                    'title': _('Processor'),
                    'url': computer_set.processor.driver_url or '-',
                },
            }

            return JsonResponse(data)
    response = JsonResponse({})
    response.status_code = 405
    return response
