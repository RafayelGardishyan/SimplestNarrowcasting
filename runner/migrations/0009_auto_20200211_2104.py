# Generated by Django 3.0.3 on 2020-02-11 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('runner', '0008_auto_20200211_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='screen',
            name='screen_pin',
            field=models.IntegerField(default=6154),
        ),
    ]
