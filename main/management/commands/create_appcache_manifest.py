from django.core.management.base import NoArgsCommand

from main.management.appcache import create_manifest


class Command(NoArgsCommand):
    help = 'Create application cache manifest file.'

    def handle_noargs(self, **options):
        create_manifest()
