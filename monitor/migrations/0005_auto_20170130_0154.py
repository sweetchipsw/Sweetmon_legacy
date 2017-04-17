# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0004_auto_20170130_0148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine',
            name='ping',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True),
        ),
    ]
