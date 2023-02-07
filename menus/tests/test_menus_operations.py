import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from menus.models import Menu
from dishes.models import Dish
import json


@pytest.mark.django_db
def test_creating_menu_without_dishes_field(
        api_client_with_credentials: APIClient,
        get_new_random_menu: dict[str, str]):
    """
    Testing creating a menu without dishes field
    """
    url = reverse('menu_detail-list')

    data = get_new_random_menu
    response = api_client_with_credentials.post(url, data=json.dumps(data), content_type='application/json')

    assert response.status_code == 201
    assert Menu.objects.filter(name=data['name']).exists()
    assert not Dish.objects.all()


@pytest.mark.django_db
def test_creating_menu_with_empty_dishes_field(
        api_client_with_credentials: APIClient,
        get_new_random_menu: dict[str, str]):
    """
    Testing creating a menu with dishes as an empty list
    """
    url = reverse('menu_detail-list')

    data = get_new_random_menu
    data.update({"dishes": []})
    response = api_client_with_credentials.post(url, data=json.dumps(data), content_type='application/json')

    assert response.status_code == 201
    assert Menu.objects.filter(name=data['name']).exists()
    assert not Dish.objects.all()


@pytest.mark.django_db
def test_creating_menu_with_dishes_field(
        api_client_with_credentials: APIClient,
        get_new_random_menu: dict[str, str],
        get_new_random_dish: dict[str, str]):
    """
    Testing creating a menu with dishes field
    """
    url = reverse('menu_detail-list')

    data = get_new_random_menu
    data.update({'dishes': [get_new_random_dish]})
    response = api_client_with_credentials.post(url, data=json.dumps(data), content_type='application/json')

    assert response.status_code == 201
    assert Menu.objects.filter(name=data['name']).exists()
    assert Dish.objects.filter(name=get_new_random_dish['name']).exists()


@pytest.mark.django_db
def test_updating_menu_without_dishes_field(
        api_client_with_credentials: APIClient,
        get_new_random_menu: dict[str, str],
        get_new_random_dish: dict[str, str],
        create_menu: Menu):
    """
    Testing updating a menu without dishes field
    """
    url = f"{reverse('menu_detail-list')}{create_menu.id}/"

    data = get_new_random_menu
    response = api_client_with_credentials.put(url, data=json.dumps(data), content_type='application/json')

    assert response.status_code == 200
    assert Menu.objects.filter(name=data['name']).exists()
    assert not Dish.objects.all()


@pytest.mark.django_db
def test_updating_menu_with_empty_dishes_field(
        api_client_with_credentials: APIClient,
        get_new_random_menu: dict[str, str],
        get_new_random_dish: dict[str, str],
        create_menu: Menu):
    """
    Testing updating a menu with empty dishes field
    """
    url = f"{reverse('menu_detail-list')}{create_menu.id}/"

    data = get_new_random_menu
    data.update({'dishes': []})
    response = api_client_with_credentials.put(url, data=json.dumps(data), content_type='application/json')

    assert response.status_code == 200
    assert Menu.objects.filter(name=data['name']).exists()
    assert not Dish.objects.all()


@pytest.mark.django_db
def test_updating_menu_with_dishes_field(
        api_client_with_credentials: APIClient,
        get_new_random_menu: dict[str, str],
        get_new_random_dish: dict[str, str],
        create_menu: Menu):
    """
    Testing updating a menu with dishes field
    """
    url = f"{reverse('menu_detail-list')}{create_menu.id}/"

    data = get_new_random_menu
    data.update({'dishes': [get_new_random_dish]})
    response = api_client_with_credentials.put(url, data=json.dumps(data), content_type='application/json')

    assert response.status_code == 200
    assert Menu.objects.filter(name=data['name']).exists()
    assert Dish.objects.filter(name=get_new_random_dish['name']).exists()
