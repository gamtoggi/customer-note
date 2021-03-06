# Generated by Django 2.1.5 on 2019-01-30 21:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0005_purchase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='contacted_at',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='unit_price',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
