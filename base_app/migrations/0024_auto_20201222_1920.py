# Generated by Django 3.1.3 on 2020-12-22 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0023_profile_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='slug',
            field=models.SlugField(max_length=255, null=True, unique=True),
        ),
    ]
