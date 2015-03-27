# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.IntegerField(default=0)),
                ('history', models.CharField(default=b'', max_length=9)),
                ('time_left', models.FloatField(default=900000.0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='game_results',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('game', models.IntegerField()),
                ('history', models.CharField(max_length=9)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='pending_games',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='scripts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=50)),
                ('location', models.CharField(default=b'', max_length=255)),
                ('wins', models.IntegerField(default=0)),
                ('losses', models.IntegerField(default=0)),
                ('draws', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='users',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_name', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=255)),
                ('email', models.CharField(default=b'', max_length=50)),
                ('ip_address', models.CharField(max_length=15)),
                ('wins', models.IntegerField(default=0)),
                ('losses', models.IntegerField(default=0)),
                ('draws', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='scripts',
            name='user_id',
            field=models.ForeignKey(to='TTT.users'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='scripts',
            unique_together=set([('user_id', 'name')]),
        ),
        migrations.AddField(
            model_name='game',
            name='ai1script',
            field=models.ForeignKey(related_name='s1', blank=True, to='TTT.scripts', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='ai2script',
            field=models.ForeignKey(related_name='s2', blank=True, to='TTT.scripts', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='player1',
            field=models.ForeignKey(related_name='p1', blank=True, to='TTT.users', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='player2',
            field=models.ForeignKey(related_name='p2', blank=True, to='TTT.users', null=True),
            preserve_default=True,
        ),
    ]
