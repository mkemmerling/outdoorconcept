import os
import shutil

from django.conf import settings
from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    help = 'Copy previously cached static files to current static cache.'

    def handle_noargs(self, **options):
        previous_cache = os.path.join(settings.DATA_DIR, 'PREVIOUS_CACHE')
        cache_dir = os.path.join(settings.STATIC_ROOT, 'CACHE')

        def copy_files(fype):
            src_dir = os.path.join(previous_cache, fype)
            dest_dir = os.path.join(cache_dir, fype)
            for name in os.listdir(src_dir):
                if name.endswith('.' + fype):
                    src = os.path.join(src_dir, name)
                    dst = os.path.join(dest_dir, name)
                    if not os.path.exists(dst):
                        shutil.copy(src, dst)

        copy_files('css')
        copy_files('js')
