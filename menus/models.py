from django.db import models
from general_utils.models import TimeStampedModel


class Menu(TimeStampedModel):

    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name
