# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0006_auto_20170130_0303'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='crash',
            name='id',
        ),
        migrations.AddField(
            model_name='crash',
            name='idx',
            field=models.AutoField(default=0, serialize=False, primary_key=True),
            preserve_default=False,
        ),
    ]
