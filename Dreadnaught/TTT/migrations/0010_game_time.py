# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TTT', '0009_auto_20150318_2301'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='time',
            field=models.DecimalField(default=900000, max_digits=20, decimal_places=20),
            preserve_default=True,
        ),
    ]
