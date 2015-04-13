# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TTT', '0002_auto_20150401_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turns',
            name='begin_state',
            field=models.CharField(default=b'', max_length=1000),
            preserve_default=True,
        ),
    ]
