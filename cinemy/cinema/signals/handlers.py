from django.db.models.signals import post_save
from django.dispatch import receiver
from cinema.models import generate_seats, Seat, Hall


@receiver(post_save, sender=Hall)
def hall_creation_handler(instance, **kwargs):
    generated_seats = generate_seats(instance.rows, instance.seats_per_row)
    instance.seats.add(*generated_seats, bulk=False)
