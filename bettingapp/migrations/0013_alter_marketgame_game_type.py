# Generated by Django 3.2.5 on 2021-08-03 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bettingapp', '0012_auto_20210802_0807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marketgame',
            name='game_type',
            field=models.CharField(default=0, max_length=250),
        ),
    ]
