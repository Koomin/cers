from django.http import JsonResponse
from django.shortcuts import render

from cers.hardware.models import ComputerSet


def driver_site(request):
    return render(request, 'custom/drivers.html')


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
                'model': computer_set.model.name,
                'operating_system': computer_set.operating_system.name,
                'motherboard': computer_set.motherboard.__str__(),
                'power_supply': computer_set.power_supply.__str__(),
                'processor': computer_set.processor.__str__(),
            }
            return JsonResponse(data)
    response = JsonResponse({})
    response.status_code = 405
    return response
