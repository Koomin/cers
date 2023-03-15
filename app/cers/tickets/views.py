from cers.tickets.models import Ticket
from django.http import JsonResponse


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
