# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TTT', '0012_auto_20150314_0614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='time',
            field=models.FloatField(),
            preserve_default=True,
        ),
    ]
