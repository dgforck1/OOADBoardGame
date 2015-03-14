# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TTT', '0013_auto_20150314_0614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='time',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
    ]
