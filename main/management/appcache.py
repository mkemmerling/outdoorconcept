"""Create appcache manifest."""
import datetime
import os
import re

from django.conf import settings

import main
import ropeelements
import siebert

MANIFEST_FILE = os.path.join(settings.STATIC_ROOT, 'cache.manifest')

CACHE_DIR = os.path.join(settings.STATIC_ROOT, 'CACHE')
MAIN_STATIC_DIR = os.path.join(os.path.dirname(main.__file__), 'static')
RE_STATIC_DIR = os.path.join(os.path.dirname(ropeelements.__file__), 'static')
SIEBERT_STATIC_DIR = os.path.join(os.path.dirname(siebert.__file__), 'static')

join = os.path.join


def create_manifest():
    """Create appcache manifest."""
    manifest = 'CACHE MANIFEST\n'
    manifest += created() + '\n\n'

    manifest += '# Templates\n'
    manifest += '/en/ropeelements\n'
    manifest += '/de/seilelemente\n'
    manifest += '/en/ng/ropeelements\n'
    manifest += '/de/ng/ropeelements\n'
    manifest += '\n'

    manifest += '# Data\n'
    manifest += '/en/api/ropeelements\n'
    # manifest += '/de/api/ropeelements\n'
    # manifest += '\n'

    manifest += '# Static files\n'

    # CSS
    if settings.COMPRESS_ENABLED:
        for name in os.listdir(join(CACHE_DIR, 'css')):
            manifest += static_file_entry(join('CACHE', 'css', name))
    else:
        subpath = join('jquery-ui', 'themes')
        manifest += static_file_entry(join(subpath, 'base', 'core.css'))
        manifest += static_file_entry(join(subpath, 'base', 'datepicker.css'))
        manifest += static_file_entry(join(subpath, 'smoothness', 'theme.css'))
        for name in os.listdir(join(CACHE_DIR, 'css')):
            if name.startswith('app.'):
                manifest += static_file_entry(join('CACHE', 'css', name))

    # JavaScripts
    if settings.COMPRESS_ENABLED:
        for name in os.listdir(join(CACHE_DIR, 'js')):
            manifest += static_file_entry(join('CACHE', 'js', name))
    else:
        manifest += static_file_entry(join('modernizr', 'modernizr.js'))
        manifest += static_file_entry(join('jquery', 'dist', 'jquery.js'))
        subpath = join('jquery-ui', 'ui')
        manifest += static_file_entry(join(subpath, 'core.js'))
        manifest += static_file_entry(join(subpath, 'datepicker.js'))
        manifest += static_file_entry(
            join(subpath, 'i18n', 'datepicker-de.js'))
        manifest += static_file_entry(join('angular', 'angular.js'))
        manifest += static_file_entry(
            join('angular-route', 'angular-route.js'))
        manifest += static_file_entry(
            join('angular-resource', 'angular-resource.js'))
        manifest += static_file_entry(
            join('angular-sanitize', 'angular-sanitize.js'))
        manifest += static_file_entry(join('bootstrap', 'js', 'modal.js'))
        manifest += collect_static(RE_STATIC_DIR, join('ropeelements', 'js'))
        manifest += collect_static(SIEBERT_STATIC_DIR, join('siebert', 'js'))
        manifest += collect_static(MAIN_STATIC_DIR, join('main', 'js'))

    # Fonts
    files = ('glyphicons-halflings-regular.' + ext
             for ext in ('ttf', 'woff', 'woff2'))
    manifest += collect_static(
        settings.STATIC_ROOT, join('bootstrap', 'fonts'), files)

    # Images
    manifest += collect_static(MAIN_STATIC_DIR, join('main', 'images'))
    manifest += collect_static(RE_STATIC_DIR, join('ropeelements', 'images'))

    manifest += '\n'

    manifest += '# Media files\n'
    len_media_root = len(settings.MEDIA_ROOT)
    for root, dirs, files in os.walk(settings.MEDIA_ROOT):
        base = join(
            settings.MEDIA_URL, root[len_media_root:].strip('/')).rstrip('/')
        names = '\n'.join(join(base, name) for name in files)
        if names:
            manifest += names + '\n'

    manifest += '\n'
    manifest += 'NETWORK:\n'
    manifest += '*\n'

    with open(MANIFEST_FILE, 'w') as fd:
        fd.write(manifest)


def static_file_entry(subpath):
    return os.path.join(settings.STATIC_URL, subpath + '\n')


def collect_static(basedir, subpath, files=None):
    dirpath = join(basedir, subpath)
    base = join(settings.STATIC_URL, subpath)
    files = files or os.listdir(dirpath)
    return collect_files(base, files)


def collect_files(base, files):
    entries = '\n'.join(
        join(base, name) for name in files if not name.startswith('.'))
    if not entries:
        return ''
    return entries + '\n'


def created():
    return '# Created {}'.format(datetime.datetime.now().isoformat())


create_pattern = re.compile(r'# Created .+')


def touch_manifest():
    """Update timestamp in appcache manifest."""

    with open(MANIFEST_FILE, 'r+t') as fd:
        manifest = fd.read()
        manifest = create_pattern.sub(created(), manifest)
        fd.seek(0)
        fd.write(manifest)


def update_manifest(recreate=False):
    create_manifest() if recreate else touch_manifest()
