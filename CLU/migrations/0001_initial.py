# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-15 19:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Build',
            fields=[
                ('buildCod', models.AutoField(primary_key=True, serialize=False)),
                ('buildName', models.CharField(max_length=100)),
                ('buildSucces', models.CharField(choices=[('S', 'Sim'), ('N', 'Nao')], max_length=1)),
                ('buildDate', models.DateTimeField(verbose_name='building date')),
            ],
        ),
    ]