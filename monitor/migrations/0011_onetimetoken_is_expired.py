# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0010_auto_20170227_1331'),
    ]

    operations = [
        migrations.AddField(
            model_name='onetimetoken',
            name='is_expired',
            field=models.BooleanField(default=False),
        ),
    ]
