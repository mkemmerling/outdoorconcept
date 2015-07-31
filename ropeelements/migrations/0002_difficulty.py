# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ropeelements', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Difficulty',
            fields=[
                ('id', models.AutoField(
                    serialize=False, auto_created=True, primary_key=True,
                    verbose_name='ID')),
                ('order', models.PositiveIntegerField(
                    db_index=True, editable=False)),
                ('identifier', models.CharField(
                    max_length=50, verbose_name='Identifier')),
                ('identifier_en', models.CharField(
                    null=True, max_length=50, verbose_name='Identifier')),
                ('identifier_de', models.CharField(
                    null=True, max_length=50, verbose_name='Identifier')),
                ('lower_bound', models.SmallIntegerField(
                    choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
                             (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)],
                    default=1, verbose_name='from')),
                ('upper_bound', models.SmallIntegerField(
                    choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
                             (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)],
                    default=10, verbose_name='to')),
            ],
            options={
                'verbose_name': 'Difficulty',
                'ordering': ('order',),
                'verbose_name_plural': 'Difficulties',
            },
        ),
    ]
