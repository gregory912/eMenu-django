from .models import Dish
from .serializers import DishSerializer
from rest_framework import generics


class DishDetail(generics.RetrieveUpdateAPIView):
    """
    The class manages to retrieve and modify the dishes
    """
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
