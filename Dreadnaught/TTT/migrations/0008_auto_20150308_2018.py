# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TTT', '0007_users_email'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='scripts',
            unique_together=set([('user_id', 'name')]),
        ),
    ]
