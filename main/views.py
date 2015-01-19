"""Main outdoorconcept views."""
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import translation


def get_ropeelement_urls():
    """Map language to rope elements view urls."""
    def get_urls():
        return {
            'index': reverse('ropeelements'),
            'offline': reverse('ropeelements_offline'),
        }
    cur_language = translation.get_language()
    try:
        translation.activate('en')
        urls_en = get_urls()
        translation.activate('de')
        urls_de = get_urls()
    finally:
        translation.activate(cur_language)
    return {
        'ropeelements_urls': {
            'en': urls_en,
            'de': urls_de,
        }
    }


def app_view(request, **kwargs):
    """App template view."""
    return render_to_response(
        'app.html', get_ropeelement_urls(), RequestContext(request))
