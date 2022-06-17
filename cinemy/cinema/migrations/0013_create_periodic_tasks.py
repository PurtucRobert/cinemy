from django.db import migrations
from django_q.tasks import schedule, Schedule


def create_periodic_tasks(apps, schema_editor):
    schedule(
        func="cinema.tasks.tasks.mark_unconfirmed_reservations_as_expired",
        name="Mark unconfirmed reservations as expired",
        minutes=1,
        repeats=-1,
        cluster="cinema",
        schedule_type=Schedule.MINUTES,
    )


class Migration(migrations.Migration):

    dependencies = [
        ("cinema", "0012_reservation_expired_alter_reservation_reserved_time"),
    ]

    operations = [
        migrations.RunPython(create_periodic_tasks),
    ]
