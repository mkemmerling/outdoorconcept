"""Create appcache manifest."""
import os

from django.conf import settings

import main
import ropeelements
import siebert

MAIN_STATIC_DIR = os.path.join(os.path.dirname(main.__file__), 'static')
MANIFEST_FILE = os.path.join(MAIN_STATIC_DIR, 'main', 'cache.manifest')
RE_STATIC_DIR = os.path.join(os.path.dirname(ropeelements.__file__), 'static')
SIEBERT_STATIC_DIR = os.path.join(os.path.dirname(siebert.__file__), 'static')
CACHE_DIR = os.path.join(settings.STATIC_ROOT, 'CACHE')

join = os.path.join


def create_manifest():
    manifest = 'CACHE MANIFEST\n'
    manifest += '# v1 TODO\n\n'

    manifest += '# Templates\n'
    manifest += '/en/ropeelements\n'
    manifest += '/de/seilelemente\n'
    manifest += '/ng/ropeelements\n'
    manifest += '\n'

    manifest += '# Data\n'
    manifest += '/api/ropeelements\n'
    manifest += '\n'

    manifest += '# Static files\n'

    # CSS
    if settings.COMPRESS_ENABLED:
        pass  # TODO: CACHE
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
        pass  # TODO: CACHE
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
