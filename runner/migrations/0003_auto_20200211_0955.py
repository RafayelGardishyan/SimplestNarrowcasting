# Generated by Django 3.0.3 on 2020-02-11 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('runner', '0002_screen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='screen',
            name='screen_pin',
            field=models.IntegerField(default=4563),
        ),
    ]
