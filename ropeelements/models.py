"""Rope element models."""
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch.dispatcher import receiver
from django.utils.translation import ugettext_lazy as _

from ordered_model.models import OrderedModel


class Config(models.Model):
    """Rope element configuration."""

    variable = models.CharField(max_length=50, verbose_name=_('Variable'))
    text = models.CharField(max_length=1000, verbose_name=_('Text'))
    url = models.URLField(verbose_name='URL')

    class Meta:
        verbose_name = _('Configuration')
        verbose_name_plural = _('Configuration')

    def __str__(self):
        return self.variable


class Difficulty(OrderedModel):
    """Rope element difficulty search configuration."""

    DIFFICULTIES = tuple([(i, i) for i in range(1, 11)])

    identifier = models.CharField(max_length=50, verbose_name=_('Identifier'))
    lower_bound = models.SmallIntegerField(
        choices=DIFFICULTIES, default=1, verbose_name=_('from'))
    upper_bound = models.SmallIntegerField(
        choices=DIFFICULTIES, default=10, verbose_name=_('to'))

    class Meta:
        ordering = ('order',)
        verbose_name = _('Difficulty')
        verbose_name_plural = _('Difficulties')

    @property
    def range(self):
        return (self.lower_bound, self.upper_bound)

    def __str__(self):
        return self.identifier


class Kind(OrderedModel):
    """The kind of a rope element."""
    title = models.CharField(_('Title'), max_length=100, unique=True)

    class Meta:
        ordering = ('order',)
        verbose_name = _('Kind')
        verbose_name_plural = _('Kinds')

    def __str__(self):
        return self.title


class ImageField(models.ImageField):
    """Extended ``ImageField``.

    Deletes existing image file before the image is deleted or updated with
    a new image.
    """

    def save_form_data(self, instance, data):
        # Mark instance if image added, updated, or deleted, inspectec by
        # the 'rebuild_appcache' post_save signal handler.
        if data is False or isinstance(data, (InMemoryUploadedFile)):
            instance._image_modified = True
        image = getattr(instance, self.name)
        if image and image is not data:
            image.delete(False)
        super(ImageField, self).save_form_data(instance, data)


class Element(OrderedModel):
    """A rope element."""

    DIRECTIONS = (
        ('owdd', _('one way downhill')),
        ('owsd', _('one way vertically down')),
        ('twud', _('vertically two way')),
        ('twudd', _('two way up or down')),
        ('twhd', _('two way horizontally or little acclivity')),
        ('twh', _('two way horizontally')),
        ('owh', _('one way horizontally')),
    )

    SSB = (
        ('no', _('no')),
        ('yes', _('yes')),
        ('powerfan', _('with POWERFAN')),
    )

    kind = models.ForeignKey(
        Kind, related_name='kinds', verbose_name=_('Kind'))
    title = models.CharField(
        max_length=255, unique=True, verbose_name=_('Title'))
    description = models.TextField(
        max_length=2000, blank=True, verbose_name=_('Description'))
    image = ImageField(
        blank=True, width_field='image_width', verbose_name=_('Image'))
    image_width = models.SmallIntegerField(null=True)
    thumbnail = ImageField(
        upload_to='thumbnails', blank=True, verbose_name=_('Thumbnail'))
    direction = models.CharField(
        max_length=100, choices=DIRECTIONS, blank=True,
        verbose_name=_('Direction'))
    difficulty_from = models.SmallIntegerField(
        null=True, blank=True, choices=Difficulty.DIFFICULTIES,
        verbose_name=_('Difficulty'))
    difficulty_to = models.SmallIntegerField(
        null=True, blank=True, choices=Difficulty.DIFFICULTIES,
        verbose_name=_('to'))
    child_friendly = models.BooleanField(
        default=False, verbose_name=_('best for kids'))
    accessible = models.BooleanField(
        default=False, verbose_name=_('best for handicapped'))
    canope = models.BooleanField(default=False, verbose_name=_('Canope walk'))
    ssb = models.CharField(
        max_length=50, choices=SSB, default='yes', verbose_name=_('SSB'))

    order_with_respect_to = 'kind'

    class Meta:
        ordering = ('kind__order', 'order')
        verbose_name = _('Element')
        verbose_name_plural = _('Elements')

    @property
    def difficulty(self):
        return {'from': self.difficulty_from, 'to': self.difficulty_to}

    def clean(self):
        if self.difficulty_to is not None:
            if self.difficulty_from is None:
                raise ValidationError(
                    _("The 'from' value for the difficulty is missing."))
            elif self.difficulty_from > self.difficulty_to:
                raise ValidationError(
                    _("The 'to' value of the difficulty must be greater or "
                      "equal its 'form' value."))

    def __str__(self):
        return self.title


@receiver(post_delete, sender=Element)
def cleanup_after_element_delete(sender, instance, **kwargs):
    """Cleanup after deleting a rope element.

    For an element with images the images are deleted, too, and the appcache
    manifest is recreated.
    Otherwise only the manifest's timestamp is updated.
    """
    recreate_manifest = instance.image or instance.thumbnail
    instance.image.delete(False)
    instance.thumbnail.delete(False)
    from main.management import appcache
    appcache.create_js_data
    appcache.update_appcache(recreate_manifest)


@receiver(post_save, sender=Element)
def update_appcache_on_element_save(sender, instance, **kwargs):
    """Rebuild or touch app cache manifest after saving a rope element.

    If an image was added, updated or deleted, the manifest is recreated,
    otherwise only its timestamp is updated.
    """
    from main.management import appcache
    appcache.create_js_data
    appcache.update_appcache(getattr(instance, '_image_modified', False))
