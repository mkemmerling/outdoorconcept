import importlib

from django.conf import settings
from django.core.management.base import CommandError

from compressor.management.commands.compress import Command as BaseCommand

from main.views import get_ropeelement_urls

# DEPRECATED


class Command(BaseCommand):
    """Overridden ``compress`` command."""

    leave_locale_alone = True

    def handle(self, *args, **options):
        try:
            self._settings = importlib.import_module('main.settings')
        except ImportError:
            raise CommandError(
                "Settings module 'main.settings' does not exist")

        return self.handle_noargs(**options)

    def handle_noargs(self, **options):
        settings.COMPRESS_ENABLED = True
        settings.COMPRESS_OFFLINE = True
        settings.COMPRESS_OFFLINE_CONTEXT = {
            'ropeelements_urls': get_ropeelement_urls()
        }
        settings.COMPRESS_URL = settings.STATIC_URL

        if 'django.contrib.staticfiles' not in settings.INSTALLED_APPS:
            settings.INSTALLED_APPS += ('django.contrib.staticfiles',)
        super(Command, self).handle_noargs(**options)
