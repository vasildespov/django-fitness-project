# Generated by Django 3.1.3 on 2020-12-22 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0024_auto_20201222_1920'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='slug',
        ),
    ]
