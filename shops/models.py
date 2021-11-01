from django.db import models
from django.utils.timezone import now

class Shop(models.Model):
    name = models.CharField(max_length=300)

    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.name