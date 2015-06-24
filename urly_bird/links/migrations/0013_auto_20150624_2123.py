# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0012_auto_20150623_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 24, 21, 23, 34, 367881, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='click',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 24, 21, 23, 34, 369078, tzinfo=utc)),
        ),
    ]
