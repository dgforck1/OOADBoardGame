# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TTT', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game_results',
            name='game',
            field=models.IntegerField(),
            preserve_default=True,
        ),
    ]
