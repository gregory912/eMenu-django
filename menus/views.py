from rest_framework import generics
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from .filters import MenuFilter
from .models import Menu
from .serializers import MenuSerializer, MenuDetailSerializer


class MenuCreateUpdateView(CreateModelMixin,
                           UpdateModelMixin,
                           viewsets.GenericViewSet):
    """
    The class manages the creation and modification of Menus
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class MenuDetailView(generics.RetrieveAPIView):
    """
    The class manages to return full menu information
    """
    permission_classes = [AllowAny]

    queryset = Menu.objects.all()
    serializer_class = MenuDetailSerializer


class MenuListView(generics.ListAPIView):
    """
    The class manages the filtering and ordering of items from the Menu table
    """
    permission_classes = [AllowAny]

    queryset = Menu.objects.annotate(num_of_dishes=Count('dish')).filter(num_of_dishes__gt=0)
    serializer_class = MenuSerializer

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ['name', 'num_of_dishes']
    filterset_class = MenuFilter
