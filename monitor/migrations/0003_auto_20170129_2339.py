# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0002_auto_20170129_2250'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthInformation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('password', models.CharField(max_length=256)),
            ],
        ),
        migrations.AlterField(
            model_name='crash',
            name='crash_hash',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='crash',
            name='fuzzer_name',
            field=models.CharField(max_length=50),
        ),
    ]
