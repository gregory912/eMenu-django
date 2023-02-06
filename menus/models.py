from django.db import models


class Menu(models.Model):

    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
