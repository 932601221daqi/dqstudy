# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-03-02 10:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TextContext',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='课程名')),
                ('content', models.TextField(verbose_name='内容')),
            ],
            options={
                'verbose_name': '课程内容',
                'verbose_name_plural': '课程内容',
                'db_table': 'course_context',
            },
        ),
        migrations.CreateModel(
            name='TextType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=128, verbose_name='课程种类')),
            ],
            options={
                'verbose_name': '课程种类',
                'verbose_name_plural': '课程种类',
                'db_table': 'course_type',
            },
        ),
        migrations.AddField(
            model_name='textcontext',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='text.TextType', verbose_name='课程种类'),
        ),
    ]
