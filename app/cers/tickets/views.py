from django.http import JsonResponse
from django.shortcuts import render

from cers.tickets.models import Ticket


def accept_ticket(request):
    if request.user.is_manager:
        pk = request.POST.get('pk')
        try:
            ticket = Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            pass
        else:
            ticket.accept()
        return JsonResponse({'status': 'Success'})
