import os
import shutil
import tempfile

from django.conf import settings
from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    help = ('Copy previously cached static files to current static cache and '
            'save current one.')

    def handle_noargs(self, **options):
        previous_cache = os.path.join(settings.DATA_DIR, 'PREVIOUS_CACHE')
        cache_dir = os.path.join(settings.STATIC_ROOT, 'CACHE')
        tempdir = tempfile.TemporaryDirectory(prefix='oc_')

        def copy_previous(fype):
            src_dir = os.path.join(previous_cache, fype)
            dest_dir = os.path.join(cache_dir, fype)
            if os.path.exists(src_dir):
                for name in os.listdir(src_dir):
                    if name.endswith('.' + fype):
                        src = os.path.join(src_dir, name)
                        dst = os.path.join(dest_dir, name)
                        if not os.path.exists(dst):
                            shutil.copy(src, dst)

        shutil.copytree(cache_dir, tempdir.name)
        if os.path.exists(previous_cache):
            copy_previous('css')
            copy_previous('js')
            shutil.rmtree(previous_cache)
            new_cache = os.path.join(tempdir.name, 'CACHE')
            shutil.copytree(new_cache, previous_cache)
