# Generated by Django 3.2.5 on 2021-07-28 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0014_alter_user_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='account_holder_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
