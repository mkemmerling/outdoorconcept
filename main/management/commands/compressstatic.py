import importlib

from django.conf import settings
from django.core.management.base import CommandError

from compressor.management.commands.compress import Command as BaseCommand

from main.views import get_ropeelement_urls


class Command(BaseCommand):
    """Overridden ``compress`` command.

    Allows to compress static files for production or any other settings
    in the development envrionment.
    """
    args = '<setting_module>'
    help = (
        "Compress content outside of the request/response cycle.\n\n"
        "Compresses content for 'production' settings by default, but may be "
        "passed the\nname of another setting module as an argument.")

    leave_locale_alone = True

    def handle(self, *args, **options):
        if len(args) > 1:
            raise CommandError("Too may arguments")
        try:
            envrionment = args[0]
        except IndexError:
            envrionment = 'production'

        module_name = 'main.settings.' + envrionment
        try:
            self._settings = importlib.import_module(module_name)
        except ImportError:
            raise CommandError(
                "Settings module '{0}' does not exist".format(module_name))

        return self.handle_noargs(**options)

    def handle_noargs(self, **options):

        def get_setting(name):
            return getattr(self._settings, name, getattr(settings, name))

        static_url = get_setting('STATIC_URL')
        compress_output_dir = get_setting('COMPRESS_OUTPUT_DIR')

        settings.COMPRESS_ENABLED = True
        settings.COMPRESS_OFFLINE = True
        settings.COMPRESS_OUTPUT_DIR = compress_output_dir
        settings.COMPRESS_OFFLINE_CONTEXT = {
            'ropeelements_urls': get_ropeelement_urls()
        }
        settings.COMPRESS_URL = static_url
        settings.STATIC_URL = static_url

        if 'django.contrib.staticfiles' not in settings.INSTALLED_APPS:
            settings.INSTALLED_APPS += ('django.contrib.staticfiles',)
        super(Command, self).handle_noargs(**options)
