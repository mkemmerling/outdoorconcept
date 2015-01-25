import os
import re
import shutil

from django.conf import settings

from compressor.management.commands import compress


class Command(compress.Command):
    help = ('Compress static css and js files.\n'
            'Appcache save, keeps previously compresse css and js files.')

    css_pattern = re.compile(r'href=\\".+?CACHE/css/(.+?\.css)\\"')
    js_pattern = re.compile(r'src=\\".+?CACHE/js/(.+?\.js)\\"')

    def handle_noargs(self, **options):
        self.previous_cache = os.path.join(settings.DATA_DIR, 'PREVIOUS_CACHE')
        self.cache_dir = os.path.join(settings.STATIC_ROOT, 'CACHE')
        # self.css_dir = os.path.join(self.cache_dir, 'css')
        # self.js_dir = os.path.join(self.cache_dir, 'js')
        # self.tempdir = tempfile.TemporaryDirectory(prefix='oc_')
        settings_ok = (
            (settings.COMPRESS_ENABLED and settings.COMPRESS_OFFLINE) or
            options.get('force'))
        # if settings_ok:
        #     # self.tempdir = tempfile.TemporaryDirectory(prefix='oc_')
        #     self.save_old_files()
        super(Command, self).handle_noargs(**options)
        if settings_ok:
            self.save_cache()

    def save_cache(self):
        shutil.rmtree(self.previous_cache, ignore_errors=True)
        shutil.copytree(self.cache_dir, self.previous_cache)
