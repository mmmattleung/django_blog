# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-05-27 03:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0004_auto_20190523_0546'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='userinfo_education_and_experience',
            field=models.TextField(blank=True, null=True, verbose_name='教育和经验'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='userinfo_portfolo',
            field=models.TextField(blank=True, null=True, verbose_name='作品'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='userinfo_skills',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='技能'),
        ),
    ]
