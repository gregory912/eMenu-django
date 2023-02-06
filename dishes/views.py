from .models import Dish
from .serializers import DishSerializer
from rest_framework import generics


class DishDetail(generics.UpdateAPIView):
    """
    The class manages to modify the dishes
    """
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
