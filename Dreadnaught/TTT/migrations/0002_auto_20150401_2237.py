# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TTT', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='moves',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('move_num', models.IntegerField(default=0)),
                ('sx', models.IntegerField(default=0)),
                ('sy', models.IntegerField(default=0)),
                ('dx', models.IntegerField(default=0)),
                ('dy', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='turns',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('turn_num', models.IntegerField(default=0)),
                ('begin_state', models.CharField(default=b'', max_length=100)),
                ('game', models.ForeignKey(related_name='g', to='TTT.game')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='game_results',
        ),
        migrations.DeleteModel(
            name='pending_games',
        ),
        migrations.AddField(
            model_name='moves',
            name='turn_num',
            field=models.ForeignKey(related_name='turn', to='TTT.turns'),
            preserve_default=True,
        ),
    ]
