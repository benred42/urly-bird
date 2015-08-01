# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0016_auto_20150625_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 1, 16, 41, 22, 822676, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='click',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 1, 16, 41, 22, 823429, tzinfo=utc)),
        ),
    ]
