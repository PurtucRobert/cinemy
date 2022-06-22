from django.db.models.signals import post_save
from django.dispatch import receiver
from cinema.models import generate_seats, Hall, Movie
from newsletter.views import send_newsletter
from newsletter.models import Newsletter


@receiver(post_save, sender=Hall)
def hall_creation_handler(instance, **kwargs):
    generated_seats = generate_seats(instance.rows, instance.seats_per_row)
    instance.seats.add(*generated_seats, bulk=False)


@receiver(post_save, sender=Movie)
def movie_adding_handler(instance, **kwargs):
    emails = Newsletter.objects.values_list("email", flat=True)
    send_newsletter(instance, emails=emails)
