# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0011_auto_20150623_1855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='click',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
