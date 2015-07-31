"""Representation of rope element models in admin interface."""
from django.contrib import admin
from django.contrib.admin import widgets
from django.db.models import ImageField
from django.utils.translation import ugettext_lazy as _

from modeltranslation.admin import TranslationAdmin
from ordered_model.admin import OrderedModelAdmin

from . import models

admin.site.site_header = _('outdoordconcept Administration')


_common_js = (
    # 'https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js',
    'jquery/dist/jquery.js',
    # 'https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.4/jquery-ui.min.js',
    'jquery-ui/jquery-ui.min.js',
    'modeltranslation/js/tabbed_translation_fields.js',
)
_common_css = {
    'screen': ('modeltranslation/css/tabbed_translation_fields.css',
               'admin/css/ropeelements/form.css',
               ),
}


class ConfigAdmin(OrderedModelAdmin, TranslationAdmin):

    class Media:
        js = _common_js
        css = _common_css

    fields = ('variable', 'text', 'url')
    list_display = ('variable',)

    def get_readonly_fields(self, request, obj=None):
        if self.has_add_permission(request):
            return ()
        else:
            return ('variable',)

    def get_actions(self, request):
        if request.user.is_superuser:
            return super(ConfigAdmin, self).get_actions(request)


admin.site.register(models.Config, ConfigAdmin)


class DifficultyAdmin(OrderedModelAdmin, TranslationAdmin):

    class Media:
        js = _common_js
        css = _common_css

    list_display = ('identifier', 'lower_bound', 'upper_bound',
                    'move_up_down_links')

admin.site.register(models.Difficulty, DifficultyAdmin)


class KindAdmin(OrderedModelAdmin, TranslationAdmin):

    class Media:
        js = _common_js
        css = _common_css

    list_display = ('title', 'move_up_down_links')

admin.site.register(models.Kind, KindAdmin)


class AdminFileWidget(widgets.AdminFileWidget):
    clear_checkbox_label = _('Delete')


class RopeElementAdmin(OrderedModelAdmin, TranslationAdmin):

    class Media:
        js = _common_js
        css = _common_css

    fields = (
        'kind', 'title', 'description', 'image', 'thumbnail', 'direction',
        ('difficulty_from', 'difficulty_to'),
        ('child_friendly', 'accessible', 'canope'),
        'ssb'
    )
    formfield_overrides = {
        ImageField: {'widget': AdminFileWidget},
    }
    list_display = ('title', 'kind', 'child_friendly',
                    'accessible', 'canope', 'move_up_down_links')

admin.site.register(models.Element, RopeElementAdmin)
