from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'', views.MenuCreateUpdateView, basename='menu_detail')

urlpatterns = [
    path('filter/', views.MenuListView.as_view(), name='menu_list_view'),
    path('detail/<int:pk>/', views.MenuDetailView.as_view(), name='menu_list_view'),
    path('', include(router.urls)),
]