from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from .models import Menu
from .serializers import MenuSerializer


class MenuDetail(CreateModelMixin,
                 UpdateModelMixin,
                 viewsets.GenericViewSet):
    """
    The class manages the creation and modification of Menus
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
