# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0009_auto_20150623_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='code',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]
