# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0003_auto_20150618_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='code',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
