# Generated by Django 3.2.5 on 2021-07-18 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_auto_20210718_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assets',
            name='icon',
            field=models.FileField(blank=True, null=True, upload_to='icon/'),
        ),
    ]
