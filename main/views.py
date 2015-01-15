"""Main outdoorconcept views."""
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils import translation


def index_view(request, **kwargs):
    """Redirect application root to rope elements."""
    # return redirect('ropeelements')
    return render_to_response(
        'app.html', {
            # 'ropeelements_urls': get_ropeelement_urls()
        }, RequestContext(request))


def get_ropeelement_urls():
    """Map language to rope elements view urls."""
    cur_language = translation.get_language()
    try:
        translation.activate('en')
        ropeelements_url_en = reverse('ropeelements')
        translation.activate('de')
        ropeelements_url_de = reverse('ropeelements')
    finally:
        translation.activate(cur_language)
    return {
        'en': ropeelements_url_en,
        'de': ropeelements_url_de,
    }


def app_view(request, **kwargs):
    """App template view."""
    return render_to_response(
        'app.html', {
            # 'ropeelements_urls': get_ropeelement_urls()
        }, RequestContext(request))
