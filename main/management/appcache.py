"""Create application cache."""
import datetime
import os
import re

from django.conf import settings
from django.utils import translation

from rest_framework.renderers import JSONRenderer

import main
import ropeelements
from ropeelements.models import Element
from ropeelements.serializers import ElementSerializer, ElementListSerializer
import siebert

MANIFEST_FILE = os.path.join(settings.STATIC_ROOT, 'oc.appcache')

CACHE_DIR = os.path.join(settings.STATIC_ROOT, 'CACHE')
MAIN_STATIC_DIR = os.path.join(os.path.dirname(main.__file__), 'static')
RE_STATIC_DIR = os.path.join(os.path.dirname(ropeelements.__file__), 'static')
SIEBERT_STATIC_DIR = os.path.join(os.path.dirname(siebert.__file__), 'static')

join = os.path.join


def create_js_data():
    """Create JavaScript offline data."""
    renderer = JSONRenderer()
    jspath = join(settings.STATIC_ROOT, 'ropeelements.js')

    def serialize(lang):
        translation.activate(lang)
        queryset = Element._default_manager.all()
        serializer = ElementSerializer(queryset)
        list_serializer = ElementListSerializer(queryset, child=serializer)
        data = list_serializer.data
        return renderer.render(data)

    def write(fd, lang):
        data = serialize(lang).replace(b"'", b"\\'").replace(b'\\"', b'\\\\"')
        fd.write(b"window.localStorage.setItem('ropeelements_" +
                 bytes(lang, 'ascii') + b"', '" + data + b"');\n")

    with open(jspath, 'bw') as fd:
        write(fd, 'en')
        write(fd, 'de')


def create_manifest():
    """Create appcache manifest."""

    manifest = 'CACHE MANIFEST\n'
    manifest += created() + '\n\n'

    manifest += '# Data\n'
    manifest += static_file_entry('ropeelements.js')
    manifest += '\n'

    manifest += '# Templates\n'
    manifest += '/en/ropeelements\n'
    manifest += '/en/ng/ropeelements\n'
    manifest += '/en/ng/offline\n'
    manifest += '/de/seilelemente\n'
    manifest += '/de/ng/ropeelements\n'
    manifest += '/de/ng/offline\n'
    manifest += '\n'

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
        manifest += static_file_entry(join('bootstrap', 'js', 'transition.js'))
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
    manifest += 'FALLBACK:\n'
    manifest += '/en/ng/siebert /en/ng/offline\n'
    manifest += '/de/ng/siebert /de/ng/offline\n'
    # Handled by 'otherwise' route
    manifest += '/ /en/ropeelements\n'

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


def update_appcache(recreate_manifest=False):
    """(Re-)Create JavaScript offline data and appcache manifest.

    If ``recreate_manifest`` is ``False`` update timestamp in manifest only.
    """
    create_js_data()
    create_manifest() if recreate_manifest else touch_manifest()
