# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0006_auto_20150623_1454'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookmark',
            old_name='URL',
            new_name='url',
        ),
    ]
