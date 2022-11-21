# Generated by Django 3.2.5 on 2021-07-08 15:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_alter_user_profile_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepositHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('transaction_time', models.TimeField(auto_now_add=True)),
                ('amount', models.FloatField(default=0.0)),
                ('bonus_amount', models.FloatField()),
                ('payment_id', models.CharField(max_length=250)),
                ('payment_mode', models.CharField(max_length=250)),
                ('payment_source', models.CharField(max_length=250)),
                ('status', models.IntegerField(choices=[(0, 'Not Done'), (1, 'Done')], default=0)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
