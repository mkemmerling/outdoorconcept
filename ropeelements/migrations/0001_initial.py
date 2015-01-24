# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ropeelements.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('variable', models.CharField(max_length=50, verbose_name='Variable')),
                ('text', models.CharField(max_length=1000, verbose_name='Text')),
                ('text_en', models.CharField(max_length=1000, verbose_name='Text', null=True)),
                ('text_de', models.CharField(max_length=1000, verbose_name='Text', null=True)),
                ('url', models.URLField(verbose_name='URL')),
                ('url_en', models.URLField(verbose_name='URL', null=True)),
                ('url_de', models.URLField(verbose_name='URL', null=True)),
            ],
            options={
                'verbose_name': 'Configuration',
                'verbose_name_plural': 'Configuration',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Element',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('order', models.PositiveIntegerField(db_index=True, editable=False)),
                ('title', models.CharField(unique=True, max_length=255, verbose_name='Title')),
                ('title_en', models.CharField(unique=True, max_length=255, verbose_name='Title', null=True)),
                ('title_de', models.CharField(unique=True, max_length=255, verbose_name='Title', null=True)),
                ('description', models.TextField(blank=True, max_length=2000, verbose_name='Description')),
                ('description_en', models.TextField(blank=True, max_length=2000, verbose_name='Description', null=True)),
                ('description_de', models.TextField(blank=True, max_length=2000, verbose_name='Description', null=True)),
                ('image', ropeelements.models.ImageField(width_field='image_width', blank=True, upload_to='', verbose_name='Image')),
                ('image_width', models.SmallIntegerField(null=True)),
                ('thumbnail', ropeelements.models.ImageField(blank=True, upload_to='thumbnails', verbose_name='Thumbnail')),
                ('direction', models.CharField(blank=True, max_length=100, verbose_name='Direction', choices=[('owdd', 'one way downhill'), ('owsd', 'one way vertically down'), ('twud', 'vertically two way'), ('twudd', 'two way up or down'), ('twhd', 'two way horizontally or little acclivity'), ('twh', 'two way horizontally'), ('owh', 'one way horizontally')])),
                ('difficulty_from', models.SmallIntegerField(blank=True, null=True, verbose_name='Difficulty', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)])),
                ('difficulty_to', models.SmallIntegerField(blank=True, null=True, verbose_name='to', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)])),
                ('child_friendly', models.BooleanField(default=False, verbose_name='best for kids')),
                ('accessible', models.BooleanField(default=False, verbose_name='best for handicapped')),
                ('canope', models.BooleanField(default=False, verbose_name='Canope walk')),
                ('ssb', models.CharField(default='yes', max_length=50, verbose_name='SSB', choices=[('no', 'no'), ('yes', 'yes'), ('powerfan', 'with POWERFAN')])),
            ],
            options={
                'verbose_name': 'Element',
                'verbose_name_plural': 'Elements',
                'ordering': ('kind__order', 'order'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Kind',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('order', models.PositiveIntegerField(db_index=True, editable=False)),
                ('title', models.CharField(unique=True, max_length=100, verbose_name='Title')),
                ('title_en', models.CharField(unique=True, max_length=100, verbose_name='Title', null=True)),
                ('title_de', models.CharField(unique=True, max_length=100, verbose_name='Title', null=True)),
            ],
            options={
                'verbose_name': 'Kind',
                'verbose_name_plural': 'Kinds',
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='element',
            name='kind',
            field=models.ForeignKey(to='ropeelements.Kind', related_name='kinds', verbose_name='Kind'),
            preserve_default=True,
        ),
    ]
