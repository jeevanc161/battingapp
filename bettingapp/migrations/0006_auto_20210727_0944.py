# Generated by Django 3.2.5 on 2021-07-27 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bettingapp', '0005_marketgame_game_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='StarLineGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Starline Games', max_length=250)),
                ('time', models.TimeField()),
                ('result_digit', models.CharField(max_length=250)),
                ('status', models.SmallIntegerField(default=1)),
            ],
        ),
        migrations.AlterField(
            model_name='jodibetting',
            name='market_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bettingapp.marketgame'),
        ),
        migrations.AlterField(
            model_name='marketgame',
            name='status',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='jodibetting',
            name='star_line_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bettingapp.starlinegame'),
        ),
    ]
