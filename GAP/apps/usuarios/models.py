from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    aviso_privacidad = models.BooleanField(default=False)
    fechaAceptaAvP = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.username