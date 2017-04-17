# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0003_auto_20170129_2339'),
    ]

    operations = [
        migrations.AddField(
            model_name='crash',
            name='crash_size',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='machine',
            name='target',
            field=models.CharField(default=datetime.datetime(2017, 1, 29, 16, 48, 53, 125517, tzinfo=utc), max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='crash',
            name='reg_date',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='reg_date',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True),
        ),
    ]
