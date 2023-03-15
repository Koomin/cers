from cers.hardware.models import ComputerSet, SerialNumber
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for computer in ComputerSet.objects.all().order_by('pk'):
            computer.serial_number = SerialNumber().generate_serial_number(computer)
            computer.save()
