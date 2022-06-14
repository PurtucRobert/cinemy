# Generated by Django 4.0.4 on 2022-06-14 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0009_cinema_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seat',
            name='hall',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seats', to='cinema.hall'),
        ),
    ]
