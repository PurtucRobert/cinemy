# Generated by Django 4.0.4 on 2022-06-03 06:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cinema', '0006_hall_rows_hall_seats_per_row_seat_is_reserved_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_reserved', models.BooleanField(default=False)),
                ('reservation_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('seat', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cinema.seat')),
            ],
        ),
    ]
