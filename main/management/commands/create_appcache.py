from django.core.management.base import NoArgsCommand

from main.management.appcache import update_appcache


class Command(NoArgsCommand):
    help = 'Create application cache manifest file.'

    def handle_noargs(self, **options):
        update_appcache(True)
