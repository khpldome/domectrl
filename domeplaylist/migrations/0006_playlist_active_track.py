# Generated by Django 2.0.1 on 2018-05-27 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domeplaylist', '0005_auto_20180225_1235'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='active_track',
            field=models.IntegerField(blank=True, default=-1, null=True),
        ),
    ]