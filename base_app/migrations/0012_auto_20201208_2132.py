# Generated by Django 3.1.3 on 2020-12-08 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0011_auto_20201203_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='cover',
            field=models.ImageField(default='cover-default.jpg', upload_to='article-covers'),
        ),
    ]