"""Rope elements app configuration."""
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class RopeElementsConfig(AppConfig):
    name = 'ropeelements'
    verbose_name = _('Rope Elements')
