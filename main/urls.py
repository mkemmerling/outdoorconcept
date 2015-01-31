"""Main URL configuration."""
import re

from django.conf import settings
from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.views.generic import RedirectView, TemplateView

from ropeelements.views import ropeelements, ElementListView

app_view = TemplateView.as_view(template_name='app.html')

urlpatterns = patterns(
    '',
    url(r'^$', RedirectView.as_view(url=_('en/ropeelements')), name='app'),

    # Single age application, routing handled by Angular
    url(r'^de/siebert$', app_view, name='siebert'),
    url(r'', include('siebert.urls')),
)

urlpatterns += i18n_patterns(
    '',
    # Single age application, routing handled by Angular
    url(_(r'^ropeelements$'), app_view, name='ropeelements'),
    url(r'^ng/ropeelements$', ropeelements, name='ropeelement_list'),
    url(r'^api/ropeelements$', ElementListView.as_view(),
        name='ropeelement-list'),

    # url(r'^offline$', app_view, name='offline'),
    url(r'^ng/offline$', TemplateView.as_view(template_name='offline.html')),

    # Django admin
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin', RedirectView.as_view(url='admin/')),
)

# Serve media files in debug mode or if explicitely requested
if settings.DEBUG or getattr(settings, 'SERVE_MEDIA', False):
    prefix = re.escape(settings.MEDIA_URL.lstrip('/'))
    urlpatterns += patterns(
        '',
        url(r'^%s(?P<path>.*)$' % prefix,
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
