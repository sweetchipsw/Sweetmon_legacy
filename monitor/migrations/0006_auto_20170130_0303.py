# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0005_auto_20170130_0154'),
    ]

    operations = [
        migrations.RenameField(
            model_name='crash',
            old_name='abstract',
            new_name='crashlog',
        ),
        migrations.AddField(
            model_name='crash',
            name='title',
            field=models.CharField(default=0, max_length=1000),
            preserve_default=False,
        ),
    ]
