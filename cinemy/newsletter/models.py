from django.db import models
from django.contrib.auth.models import User


class Newsletter(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    email = models.EmailField(max_length=40, null=False)

    def __str__(self):
        return self.email
