from django.db.models.signals import post_save
from django.dispatch import receiver
from cinema.models import generate_seats, Seat, Hall


@receiver(post_save, sender=Hall)
def hall_creation_handler(instance, **kwargs):
    generated_seats = generate_seats(instance.rows, instance.seats_per_row)
    for i in range(len(generated_seats)):
        generated_seats[i].hall = instance
    Seat.objects.bulk_create(generated_seats)
