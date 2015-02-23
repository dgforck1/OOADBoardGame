# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TTT', '0003_auto_20150219_0028'),
    ]

    operations = [
        migrations.AddField(
            model_name='scripts',
            name='location',
            field=models.CharField(default=b'', max_length=255),
            preserve_default=True,
        ),
    ]
