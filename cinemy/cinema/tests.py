from django.test import TestCase
from cinema.models import generate_seats


class SeatGenerationTest(TestCase):
    def test_seat_generation(self):
        generated_seats = generate_seats(2, 2)
        self.assertEqual(
            ["1A", "2A", "1B", "2B"], [seat.name for seat in generated_seats]
        )
