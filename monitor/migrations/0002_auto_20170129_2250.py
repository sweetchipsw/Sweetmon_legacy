# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='crash',
            name='reproducable',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='crash',
            name='reg_date',
            field=models.DateTimeField(verbose_name=b'Registed date'),
        ),
        migrations.AlterField(
            model_name='machine',
            name='reg_date',
            field=models.DateTimeField(verbose_name=b'Registed date'),
        ),
    ]
