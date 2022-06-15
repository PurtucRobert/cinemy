from django.utils import timezone
from cinema.models import PlayingTime
from django.db.models import F
from datetime import timedelta


def clean_unconfirmed_reservations():
    """
    This function will clean all the unconfirmed reservations
    at 30 minutes prior to starting the movie
    """
    time_now = timezone.now()
    playing_times = PlayingTime.objects.annotate(
        time_min=(time_now - F("start_time"))
    ).filter(time_min__lte=timedelta(minutes=30))
    for playing_time in playing_times:
        playing_time.reservations.filter(confirmed=False).delete()


def clean_passed_playing_times():
    """
    This function will clean all the playing times
    of a movie that passed
    """
    PlayingTime.objects.filter(start_time__lte=timezone.now()).delete()
