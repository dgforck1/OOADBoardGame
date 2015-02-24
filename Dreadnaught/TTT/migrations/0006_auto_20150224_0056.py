# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TTT', '0005_auto_20150224_0053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='history',
            field=models.CharField(default=b'', max_length=9),
            preserve_default=True,
        ),
    ]
