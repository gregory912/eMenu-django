from django.urls import path

from . import views

urlpatterns = [
    path('<int:pk>/', views.DishDetail.as_view(), name='dish_detail'),
]
