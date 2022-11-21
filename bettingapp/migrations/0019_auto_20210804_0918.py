# Generated by Django 3.2.5 on 2021-08-04 09:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bettingapp', '0018_auto_20210804_0913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userwinner',
            name='market_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='winner_market_game', to='bettingapp.marketgame'),
        ),
        migrations.AlterField(
            model_name='userwinner',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='winner_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
