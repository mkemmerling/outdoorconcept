"""Rope elements URL configuration."""
from django.conf.urls import patterns
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = patterns(
    '',
    # url(r'^ng/siebert$', views.siebert, name='siebert_form'),
    url(r'^ng/siebert$', TemplateView.as_view(template_name='siebert.html'),
        name='siebert_form'),
    url(r'de/siebert/siebert.pdf$', views.siebert_pdf),
)
