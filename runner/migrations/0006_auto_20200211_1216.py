# Generated by Django 3.0.3 on 2020-02-11 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('runner', '0005_auto_20200211_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='screen',
            name='scroll_text',
            field=models.CharField(default='scrollllllll', max_length=255, verbose_name='Scrolling text'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='screen',
            name='screen_pin',
            field=models.IntegerField(default=4407),
        ),
    ]
