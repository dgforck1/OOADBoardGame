# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TTT', '0004_scripts_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scripts',
            name='name',
            field=models.CharField(default=b'', max_length=50),
            preserve_default=True,
        ),
    ]
