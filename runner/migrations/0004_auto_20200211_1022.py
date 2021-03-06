# Generated by Django 3.0.3 on 2020-02-11 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('runner', '0003_auto_20200211_0955'),
    ]

    operations = [
        migrations.AddField(
            model_name='screen',
            name='time',
            field=models.IntegerField(default=5000, verbose_name='Timeout (for images and HTML pages)'),
        ),
        migrations.AlterField(
            model_name='screen',
            name='screen_pin',
            field=models.IntegerField(default=8626),
        ),
    ]
