import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from dishes.models import Dish


@pytest.mark.django_db
def test_update_dish_using_put(api_client_with_credentials: APIClient,
                               get_new_random_dish: dict[str, str], create_dish: Dish):
    """
    Testing dish update via PUT method
    """
    url = reverse('dish_detail', args=[create_dish.id])

    data = get_new_random_dish
    response = api_client_with_credentials.put(url, data=data)

    assert response.status_code == 200
    assert Dish.objects.filter(name=data['name']).exists()


@pytest.mark.django_db
def test_update_dish_using_patch(api_client_with_credentials: APIClient,
                                 get_new_random_dish: dict[str, str], create_dish: Dish):
    """
    Testing dish update via PATCH method
    """
    url = reverse('dish_detail', args=[create_dish.id])

    data = {"name": "The new name"}
    response = api_client_with_credentials.patch(url, data=data)

    assert response.status_code == 200
    assert Dish.objects.filter(name=data['name']).exists()


@pytest.mark.django_db
def test_update_dish_using_put_for_incorrect_preparation_time_field(
        api_client_with_credentials: APIClient, get_new_random_dish: dict[str, str], create_dish: Dish):
    """
    Testing dish update via PUT method for a preparation time greater than 90
    """
    url = reverse('dish_detail', args=[create_dish.id])

    data = get_new_random_dish
    data['preparation_time'] = 91
    response = api_client_with_credentials.put(url, data=data)

    assert response.status_code == 400
