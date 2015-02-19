# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TTT', '0002_auto_20150217_1653'),
    ]

    operations = [
        migrations.CreateModel(
            name='game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.IntegerField(default=0)),
                ('history', models.CharField(max_length=9)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='scripts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
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
                ('password', models.CharField(max_length=50)),
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
