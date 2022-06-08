from django.db import models
from cinema.models import Cinema


class Contact(models.Model):
    from_email = models.EmailField(max_length=40, null=False)
    name = models.CharField(max_length=40, null=False)
    subject = models.CharField(max_length=50, null=False)
    message = models.CharField(max_length=500, null=False)
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=20)
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)

    def __str__(self):
        return self.cinema.name

    class Meta:
        ordering = ("name",)
