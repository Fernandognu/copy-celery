# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-16 04:12

# this file is auto-generated so don't do flake8 on it
# flake8: noqa

from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_celery_results', '0003_auto_20181106_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskresult',
            name='content_encoding',
            field=models.CharField(help_text='The encoding used to save the result data', max_length=64, verbose_name='Result Encoding'),
        )
        migrations.AlterField(
            model_name='taskresult',
            name='content_type',
            field=models.CharField(help_text='Content type of the result data', max_length=128, verbose_name='Result Content Type'),
        )
        migrations.AlterField(
            model_name='taskresult',
            name='date_done',
            field=models.DateTimeField(auto_now=True, db_index=True, help_text='Datetime field when the task was completed in UTC', verbose_name='Completed DateTime'),
        ),
        migrations.AlterField(
            model_name='taskresult',
            name='hidden',
            field=models.BooleanField(db_index=True, default=False, editable=False, help_text='Soft Delete flag that can be used instead of full delete', verbose_name='Hidden'),
        ),
        migrations.AlterField(
            model_name='taskresult',
            name='meta',
            field=models.TextField(default=None, editable=False, help_text='JSON meta information about the task, such as information on child tasks', null=True, verbose_name='Task Meta Information'),
        ),
        migrations.AlterField(
            model_name='taskresult',
            name='result',
            field=models.TextField(default=None, editable=False, help_text='The data returned by the task.  Use content_encoding and content_type fields to read.', null=True, verbose_name='Result Data'),
        ),
        migrations.AlterField(
            model_name='taskresult',
            name='status',
            field=models.CharField(choices=[('FAILURE', 'FAILURE'), ('PENDING', 'PENDING'), ('RECEIVED', 'RECEIVED'), ('RETRY', 'RETRY'), ('REVOKED', 'REVOKED'), ('STARTED', 'STARTED'), ('SUCCESS', 'SUCCESS')], db_index=True, default='PENDING', help_text='Current state of the task being run', max_length=50, verbose_name='Task State'),
        ),
        migrations.AlterField(
            model_name='taskresult',
            name='task_args',
            field=models.TextField(help_text='JSON representation of the positional arguments used with the task', null=True, verbose_name='Task Positional Arguments'),
        ),
        migrations.AlterField(
            model_name='taskresult',
            name='task_id',
            field=models.CharField(
                db_index=True,
                help_text='Celery ID for the Task that was run',
                max_length=getattr(
                    settings,
                    'DJANGO_CELERY_RESULTS_TASK_ID_MAX_LENGTH',
                    255
                ),
                unique=True,
                verbose_name='Task ID'
            ),
        ),
        migrations.AlterField(
            model_name='taskresult',
            name='task_kwargs',
            field=models.TextField(help_text='JSON representation of the named arguments used with the task', null=True, verbose_name='Task Named Arguments'),
        ),
        migrations.AlterField(
            model_name='taskresult',
            name='task_name',
            field=models.CharField(db_index=True, help_text='Name of the Task which was run', max_length=255, null=True, verbose_name='Task Name'),
        ),
        migrations.AlterField(
            model_name='taskresult',
            name='traceback',
            field=models.TextField(blank=True, help_text='Text of the traceback if the task generated one', null=True, verbose_name='Traceback'),
        ),
    ]