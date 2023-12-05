# hubspot_integration/models.py

from django.db import models

class HubspotUser(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    # Otros campos y métodos según sea necesario

    def __str__(self):
        return f"{self.firstname} {self.lastname} ({self.email})"
