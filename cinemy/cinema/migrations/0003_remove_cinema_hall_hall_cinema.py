# Generated by Django 4.0.4 on 2022-06-02 06:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0002_hall_seat_cinema'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cinema',
            name='hall',
        ),
        migrations.AddField(
            model_name='hall',
            name='cinema',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cinema.cinema'),
            preserve_default=False,
        ),
    ]
