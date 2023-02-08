import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from menus.models import Menu
from dishes.models import Dish
from random import randint
from datetime import datetime, timedelta


@pytest.mark.django_db
def test_filtering_by_name_field_ramen(api_client: APIClient, create_menu_data: None):
    """
    Test that filtering for the word RAMEN returns the correct items
    """
    url = f"{reverse('menu_filter')}?name=RAMEN"

    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'RAMEN'


@pytest.mark.django_db
def test_filtering_by_name_field_breakfest(api_client: APIClient, create_menu_data: None):
    """
    Test that filtering for the word BREAKFAST returns the correct items
    """
    url = f"{reverse('menu_filter')}?name=BREAKFAST"

    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]['name'].startswith('BREAKFAST')


@pytest.mark.django_db
def test_filtering_by_addition_period_for_dates_in_range(api_client: APIClient, create_menu_data: None):
    """
    Test filtering by addition period for dates that fall within this period
    """
    created_from = (datetime.today() - timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
    created_up_to = (datetime.today() + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')

    url = f"{reverse('menu_filter')}?created_from={created_from}&created_up_to={created_up_to}"

    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 5


@pytest.mark.django_db
def test_filtering_by_addition_period_for_dates_not_in_range(api_client: APIClient, create_menu_data: None):
    """
    Test filtering by addition period for dates that do not fall within that period
    """
    created_from = (datetime.today() - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
    created_up_to = (datetime.today() - timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')

    url = f"{reverse('menu_filter')}?created_from={created_from}&created_up_to={created_up_to}"

    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 0


@pytest.mark.django_db
def test_ordering_by_list_name(api_client: APIClient, create_menu_data: None):
    """
    Test ordering by element name
    Test checks that items are arranged in alphabetical order
    """
    url = f"{reverse('menu_filter')}?ordering=name"

    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data[0]['name'] == 'BREAKFAST DISHES'
    assert response.data[-1]['name'] == 'RAMEN'


@pytest.mark.django_db
def test_reverse_ordering_by_list_name(api_client: APIClient, create_menu_data: None):
    """
    Test reverse ordering by element name
    Test checks whether items are arranged in reverse alphabetical order
    """
    url = f"{reverse('menu_filter')}?ordering=-name"

    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data[0]['name'] == 'RAMEN'
    assert response.data[-1]['name'] == 'BREAKFAST DISHES'


@pytest.mark.django_db
def test_ordering_by_number_of_dishes(api_client: APIClient, create_menu_data: None):
    """
    Test ordering by number of dishes
    The function checks whether the number of dishes for the menu in the first
    and last place changes in ascending order
    """
    url = f"{reverse('menu_filter')}?ordering=num_of_dishes"

    response = api_client.get(url)

    assert response.status_code == 200

    items = [item['id'] for item in response.data]
    assert Dish.objects.filter(menu=items[0]).count() <= Dish.objects.filter(menu=items[-1]).count()


@pytest.mark.django_db
def test_reverse_ordering_by_number_of_dishes(api_client: APIClient, create_menu_data: None):
    """
    Test reverse ordering by number of dishes
    The function checks whether the number of dishes for the menu in the first
    and last place changes in a decreasing manner
    """
    url = f"{reverse('menu_filter')}?ordering=-num_of_dishes"

    response = api_client.get(url)

    assert response.status_code == 200

    items = [item['id'] for item in response.data]
    assert Dish.objects.filter(menu=items[0]).count() >= Dish.objects.filter(menu=items[-1]).count()


@pytest.fixture
def create_menu_data(get_new_random_menu: dict[str, str], get_new_random_dish: dict[str, str]) -> None:
    """
    Function creates random data outside of name fields and adds it to the database for testing purposes
    """
    dish_names = [
        'Spaghetti', 'Beef Stroganoff', 'Reuben', 'Waldorf Salad', 'Salisbury Steak',
        'Caesar Salad', 'Chicken à la King', 'Lobster Newburg', 'Baked Alaska'
    ]
    dishes = [get_new_random_dish.copy() for _ in range(10)]
    [dishes[counter].update({'name': dish}) for counter, dish in enumerate(dish_names)]

    menu_names = [
        'RAMEN', 'HOUSE-MADE STEAMED BUNS', 'EVERYTHING ELSE', 'BREAKFAST SANDWICHES', 'BREAKFAST DISHES'
    ]

    menus = [get_new_random_menu.copy() for _ in range(5)]
    [menus[counter].update({'name': menu}) for counter, menu in enumerate(menu_names)]

    [menu.update({'dishes': dishes[0: randint(1, 9)]}) for menu in menus]

    for counter, menu in enumerate(menus):
        instance = Menu.objects.create(name=menu['name'], description=menu['description'])
        for single_dish in menu['dishes']:
            single_dish.update({'menu': instance})
            Dish.objects.create(**single_dish)
