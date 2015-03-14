# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TTT', '0011_auto_20150314_0612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='time',
            field=models.FloatField(default=900000.0),
            preserve_default=True,
        ),
    ]
