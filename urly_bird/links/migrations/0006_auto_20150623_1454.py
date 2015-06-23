# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0005_auto_20150622_0012'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookmark',
            old_name='url',
            new_name='URL',
        ),
    ]
