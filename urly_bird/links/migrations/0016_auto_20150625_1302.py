# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0015_auto_20150625_0122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 25, 13, 2, 6, 937341, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='click',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 25, 13, 2, 6, 938163, tzinfo=utc)),
        ),
    ]
