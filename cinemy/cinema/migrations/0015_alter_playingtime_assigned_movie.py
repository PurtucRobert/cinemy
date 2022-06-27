# Generated by Django 4.0.4 on 2022-06-24 11:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cinema", "0014_seat_occupied"),
    ]

    operations = [
        migrations.AlterField(
            model_name="playingtime",
            name="assigned_movie",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="playing_times",
                to="cinema.movie",
            ),
        ),
    ]