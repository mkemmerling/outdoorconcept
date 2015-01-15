"""Translation registrations for ropeelements models."""

from modeltranslation.translator import translator, TranslationOptions
from . import models


class ConfigTranslationOptions(TranslationOptions):
    fields = ('url', 'text')

translator.register(models.Config, ConfigTranslationOptions)


class KindTranslationOptions(TranslationOptions):
    fields = ('title',)

translator.register(models.Kind, KindTranslationOptions)


class ElementTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

translator.register(models.Element, ElementTranslationOptions)
