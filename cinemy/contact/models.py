from django.db import models


class Contact(models.Model):
    from_email = models.EmailField(max_length=40, null=False)
    name = models.CharField(max_length=40, null=False)
    subject = models.CharField(max_length=50, null=False)
    message = models.CharField(max_length=500, null=False)
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=20)
    cinema = models.CharField(max_length=40)
