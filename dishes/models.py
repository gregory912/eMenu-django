from django.db import models
from menus.models import Menu


class Dish(models.Model):

    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    preparation_time = models.IntegerField()
    is_vegetarian = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
