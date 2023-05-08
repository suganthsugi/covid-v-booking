# Generated by Django 4.2 on 2023-05-07 17:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_remove_vaccinecentre_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('available_slots', models.PositiveSmallIntegerField(default=10)),
                ('vaccine_centre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.vaccinecentre')),
            ],
        ),
    ]
