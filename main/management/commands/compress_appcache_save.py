import os
import shutil

from django.conf import settings

from compressor.management.commands import compress


class Command(compress.Command):
    help = ('Compress static css and js files.\n'
            'Appcache save, keeps previously compresse css and js files.')

    def handle_noargs(self, **options):
        super(Command, self).handle_noargs(**options)
        self.save_cache()

    def save_cache(self):
        previous_cache = os.path.join(settings.DATA_DIR, 'PREVIOUS_CACHE')
        cache_dir = os.path.join(settings.STATIC_ROOT, 'CACHE')
        shutil.rmtree(previous_cache, ignore_errors=True)
        shutil.copytree(cache_dir, self.previous_cache)
