# Generated by Django 4.1 on 2023-11-29 14:20

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="measurement",
            old_name="current",
            new_name="current_mA",
        ),
        migrations.RenameField(
            model_name="measurement",
            old_name="power",
            new_name="set_power_W",
        ),
        migrations.RenameField(
            model_name="measurement",
            old_name="voltage",
            new_name="voltage_V",
        ),
    ]
