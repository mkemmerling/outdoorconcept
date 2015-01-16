"""Main URL configuration."""
import re

from django.conf import settings
from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.views.generic import RedirectView

from main import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index_view, name='app'),
    # Single age application, routing handled by Angular
    url(r'^de/siebert$', views.app_view, name='siebert'),
    url(r'', include('ropeelements.urls')),
    url(r'', include('siebert.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
)

urlpatterns += i18n_patterns(
    '',
    # Single age application, routing handled by Angular
    url(_(r'^ropeelements$'), views.app_view, name='ropeelements'),
    # Django admin
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin', RedirectView.as_view(url='admin/')),
)

# Serve media files in debug mode or if explicitely requested
# if settings.DEBUG or getattr(settings, 'SERVE_MEDIA', False):
#     prefix = re.escape(settings.MEDIA_URL.lstrip('/'))
#     urlpatterns += patterns(
#         '',
#         url(r'^%s(?P<path>.*)$' % prefix,
#             'django.views.static.serve',
#             {'document_root': settings.MEDIA_ROOT}),
#     )
