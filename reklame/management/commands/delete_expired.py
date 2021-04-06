from django.core.management.base import BaseCommand
from django.utils import timezone

from reklame.models import Reklame


class Command(BaseCommand):
    help = 'Deletes expired rows'

    def handle(self, *args, **options):
        now = timezone.now()
        Reklame.objects.filter(expired__lt=now).delete()
