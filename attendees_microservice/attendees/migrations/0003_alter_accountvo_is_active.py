# Generated by Django 4.0.3 on 2022-04-22 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendees', '0002_accountvo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountvo',
            name='is_active',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]