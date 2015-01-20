"""Rope element serializers."""
from collections import OrderedDict

from rest_framework import serializers

from . import models


class KindSerializer(serializers.ModelSerializer):
    """Rope element kind serializer."""

    class Meta:
        model = models.Kind
        fields = ('id', 'title')


class ElementListSerializer(serializers.ListSerializer):
    """Rope element list serializer."""

    def to_representation(self, data):
        kind_serializer = KindSerializer()
        by_kind = OrderedDict()
        for item in data:
            kind_elements = by_kind.setdefault(item.kind, [])
            kind_elements.append(self.child.to_representation(item))
        return [{
            'kind': kind_serializer.to_representation(kind),
            'elements': elements
        } for (kind, elements) in by_kind.items()]


class ElementSerializer(serializers.ModelSerializer):
    """Rope element serializer."""

    direction_title = serializers.CharField(source='get_direction_display',
                                            read_only=True)

    class Meta:
        model = models.Element
        fields = (
            'title', 'description',
            'image', 'image_width', 'thumbnail',
            'direction', 'direction_title', 'difficulty',
            'child_friendly', 'accessible', 'canope', 'ssb'
        )
        list_serializer_class = ElementListSerializer
