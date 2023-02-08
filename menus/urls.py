from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'', views.MenuCreateUpdateView, basename='menu_create_update')

urlpatterns = [
    path('filter/', views.MenuListView.as_view(), name='menu_filter'),
    path('detail/<int:pk>/', views.MenuDetailView.as_view(), name='menu_detail'),
    path('', include(router.urls)),
]