# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-22 14:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uf', models.CharField(max_length=2)),
                ('cnl', models.CharField(max_length=4)),
                ('cnl_code', models.CharField(max_length=5)),
                ('locality', models.CharField(max_length=50)),
                ('municipality', models.CharField(max_length=50)),
                ('tax_area_code', models.CharField(max_length=5)),
                ('prefix', models.CharField(max_length=7)),
                ('provider', models.CharField(max_length=30)),
                ('initial_interval_number', models.CharField(max_length=4)),
                ('final_interval_number', models.CharField(max_length=4)),
                ('latitude', models.CharField(max_length=8)),
                ('hemisphere', models.CharField(max_length=5)),
                ('longitude', models.CharField(max_length=8)),
                ('local_area_cnl', models.CharField(max_length=4)),
            ],
        ),
    ]
