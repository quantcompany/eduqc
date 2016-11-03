# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-02 15:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sesiones', '0003_enrollment_transaction'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='enrollment',
            options={'ordering': ['last_modified', 'enrollment_date']},
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='sesiones.Session'),
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='users.Student'),
        ),
    ]