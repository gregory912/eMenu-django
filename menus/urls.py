from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'', views.MenuDetail, basename='menu_detail')

urlpatterns = [
    path('', include(router.urls)),
]