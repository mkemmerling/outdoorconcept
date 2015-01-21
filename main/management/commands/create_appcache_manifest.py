from django.core.management.base import BaseCommand

from main.management.appcache import create_manifest


class Command(BaseCommand):
    help = 'Create application cache manifest file.'

    def handle(self, *args, **options):
        create_manifest()
