"""Main outdoorconcept views."""
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import translation


def get_ropeelement_url():
    """Map language to rope elements view urls."""
    cur_language = translation.get_language()
    try:
        translation.activate('en')
        url_en = reverse('ropeelements')
        translation.activate('de')
        url_de = reverse('ropeelements')
    finally:
        translation.activate(cur_language)
    return {
        'ropeelements_url': {
            'en': url_en,
            'de': url_de,
        }
    }


def app_view(request, **kwargs):
    """App template view."""
    return render_to_response(
        'app.html', get_ropeelement_url(), RequestContext(request))
