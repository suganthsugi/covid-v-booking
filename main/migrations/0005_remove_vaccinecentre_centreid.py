# Generated by Django 4.2 on 2023-05-07 10:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_rename_dsitrict_vaccinecentre_district'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vaccinecentre',
            name='centreid',
        ),
    ]
