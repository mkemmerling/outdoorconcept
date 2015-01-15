# encoding: utf-8
"""Rope element sample data factories."""
import importlib
import json
import os

import factory

from . import models

fixtures_dir = os.path.join(os.path.dirname(
    importlib.import_module('ropeelements').__file__), 'fixtures')


def load(name):
    with open(os.path.join(fixtures_dir, name + '.json'), 'r') as fd:
        return json.loads(fd.read())


class ConfigFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Config


def create_config():
    [ConfigFactory.create(**data) for data in load('config')]


class KindFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Kind

    title_en = 'Seilrutschen'
    title_de = 'Zip Lines & Downward'


def create_kinds():
    [KindFactory.create(**data) for data in load('kinds')]


def find_or_create_kind(title_en):
    try:
        return models.Kind.objects.get(title_en=title_en)
    except models.Kind.DoesNotExist:
        return KindFactory.create(title_en=title_en)


def image_path(filename):
    return os.path.normpath(os.path.join(fixtures_dir, 'images', filename))


class ElementFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Element

    image = factory.django.ImageField()
    thumbnail = factory.django.ImageField()


def create_element(**data):
    data['kind'] = find_or_create_kind(data.pop('kind_en'))
    if 'image' in data:
        data['image__from_path'] = image_path(data['image'])
        del data['image']
    else:
        data['image'] = None
    if 'thumbnail' in data:
        data['thumbnail__from_path'] = image_path(data['thumbnail'])
        del data['thumbnail']
    else:
        data['thumbnail'] = None

    ElementFactory.create(**data)


def create_elements():
    [create_element(**data) for data in load('elements')]
