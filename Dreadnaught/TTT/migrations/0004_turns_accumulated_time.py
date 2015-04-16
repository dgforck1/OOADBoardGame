# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TTT', '0003_auto_20150409_0613'),
    ]

    operations = [
        migrations.AddField(
            model_name='turns',
            name='accumulated_time',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
    ]
