# Generated by Django 4.2.2 on 2023-07-24 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filling_station', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fillingstation',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
