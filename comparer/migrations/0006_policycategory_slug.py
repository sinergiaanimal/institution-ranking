# Generated by Django 3.1.12 on 2021-07-08 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comparer', '0005_auto_20210707_1343'),
    ]

    operations = [
        migrations.AddField(
            model_name='policycategory',
            name='slug',
            field=models.SlugField(default='default', verbose_name='slug'),
            preserve_default=False,
        ),
    ]
