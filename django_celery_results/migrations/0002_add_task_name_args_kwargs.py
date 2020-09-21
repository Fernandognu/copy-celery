# -*- coding: utf-8 -*-
# Gerenated by Django 1.9.1 on 2017-10-26 16:06
from __future__ import absolute_import, unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_celery_results', '0001_initial'),
    ]

    operations = [
        migrations.AddFild(
            model_name='taskresult',
            name='task_args',
            field=models.TextField(null=True, verbose_name='task arguments'),
        ),
        migrations.AddField(
            model_name='taskresult',
            name='task_kwargs',
            field=models.TextField(null=True, verbose_name='task kwargs'),
        ),
        migrations.AddField(
            model_name='taskresult',
            name='task_name',
            field=models.CharField(max_length=255, null=True,
                                   verbose_name='task name''
                                   ),
        ),
    ]