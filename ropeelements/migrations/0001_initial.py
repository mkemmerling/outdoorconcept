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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('variable', models.CharField(verbose_name='Variable', max_length=50)),
                ('text', models.CharField(verbose_name='Text', max_length=1000)),
                ('text_en', models.CharField(null=True, verbose_name='Text', max_length=1000)),
                ('text_de', models.CharField(null=True, verbose_name='Text', max_length=1000)),
                ('url', models.URLField(verbose_name='URL')),
                ('url_en', models.URLField(null=True, verbose_name='URL')),
                ('url_de', models.URLField(null=True, verbose_name='URL')),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title', unique=True)),
                ('title_en', models.CharField(null=True, max_length=255, verbose_name='Title', unique=True)),
                ('title_de', models.CharField(null=True, max_length=255, verbose_name='Title', unique=True)),
                ('description', models.TextField(blank=True, verbose_name='Description', max_length=2000)),
                ('description_en', models.TextField(null=True, blank=True, verbose_name='Description', max_length=2000)),
                ('description_de', models.TextField(null=True, blank=True, verbose_name='Description', max_length=2000)),
                ('image', ropeelements.models.ImageField(blank=True, width_field='image_width', verbose_name='Image', upload_to='')),
                ('image_width', models.SmallIntegerField(null=True)),
                ('thumbnail', ropeelements.models.ImageField(blank=True, verbose_name='Thumbnail', upload_to='thumbnails')),
                ('direction', models.CharField(choices=[('down', 'one way downhill'), ('vertical_down', 'one way vertically down'), ('horizontal', 'two way horicontally'), ('little_acclivity', 'two way horicontally or little acclivity')], blank=True, verbose_name='Direction', max_length=100)),
                ('difficulty_from', models.SmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], null=True, verbose_name='Difficulty', blank=True)),
                ('difficulty_to', models.SmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], null=True, verbose_name='to', blank=True)),
                ('child_friendly', models.BooleanField(verbose_name='Best for kids', default=False)),
                ('accessible', models.BooleanField(verbose_name='Best for handicapped ', default=False)),
                ('canope', models.BooleanField(verbose_name='Canope Walk', default=False)),
                ('ssb', models.CharField(choices=[('no', 'no'), ('yes', 'yes'), ('powerfan', 'with POWERFAN')], verbose_name='SSB', max_length=50, default='yes')),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('title', models.CharField(max_length=100, verbose_name='Title', unique=True)),
                ('title_en', models.CharField(null=True, max_length=100, verbose_name='Title', unique=True)),
                ('title_de', models.CharField(null=True, max_length=100, verbose_name='Title', unique=True)),
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
            field=models.ForeignKey(verbose_name='Kind', to='ropeelements.Kind', related_name='kinds'),
            preserve_default=True,
        ),
    ]
