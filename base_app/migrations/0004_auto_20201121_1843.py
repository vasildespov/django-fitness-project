# Generated by Django 3.1.3 on 2020-11-21 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0003_article_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='cover',
            field=models.ImageField(default='cover-default.jpg', null=True, upload_to='article-covers'),
        ),
    ]