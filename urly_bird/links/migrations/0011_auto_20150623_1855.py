# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0010_auto_20150623_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='code',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]
