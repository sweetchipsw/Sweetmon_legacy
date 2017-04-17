# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0007_auto_20170130_0311'),
    ]

    operations = [
        migrations.AddField(
            model_name='crash',
            name='crash_file',
            field=models.FileField(default='', storage=django.core.files.storage.FileSystemStorage(location=b'/home/sweetchip/sweetboard/sweetmon/private'), upload_to=b''),
            preserve_default=False,
        ),
    ]
