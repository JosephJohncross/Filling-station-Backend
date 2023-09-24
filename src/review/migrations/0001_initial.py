# Generated by Django 4.2.2 on 2023-09-23 17:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('filling_station', '0006_alter_fillingstation_car_mechanic_and_more'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.CharField()),
                ('date_of_review', models.DateField(auto_now_add=True)),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='filling_station.fillingstation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.generaluser')),
            ],
        ),
    ]