import pytest
from rest_framework.test import APIClient
from faker import Faker
from typing import Callable
from users.models import User
from menus.models import Menu
from dishes.models import Dish
from random import randint


@pytest.fixture
def api_client() -> APIClient:
    """
    The function returns APIClient object
    """
    return APIClient()


@pytest.fixture
def api_client_with_credentials(db, create_user: User, api_client: APIClient) -> APIClient:
    """
    The function returns an APIClient object. The user has been authenticated.
    By using yield the credentials will be cleared after each test
    """
    user = create_user
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)


@pytest.fixture
def faker() -> Faker:
    """
    The function returns Faker object
    """
    return Faker()


@pytest.fixture
def create_user(db) -> User:
    """
    The function creates a new user for the sample data
    """
    return User.objects.create_user(
        username="test-user",
        password="test"
    )


@pytest.fixture
def create_user_data(db) -> Callable[[str], dict[str, str]]:
    """
    The function through closure returns a function that we can call with our data
    """
    def create_clousure_user(username: str, password: str, first_name: str, last_name: str, email: str,
                             is_staff: str = False, is_superuser: str = False, is_active: str = True) -> dict[str, str]:
        return {
            "username": username,
            "first_name": first_name,
            "password": password,
            "password_confirmation": password,
            "last_name": last_name,
            "email": email,
            "is_staff": is_staff,
            "is_superuser": is_superuser,
            "is_active": is_active}

    return create_clousure_user


@pytest.fixture
def get_new_random_user(create_user_data: Callable, faker: Faker) -> dict[str, str]:
    """
    The function creates a user with random data
    """
    return create_user_data(
        username=faker.word(),
        password=faker.password(),
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        email=faker.email()
    )


@pytest.fixture
def create_menu(db) -> Menu:
    """
    The function creates a new menu for the sample data
    """
    return Menu.objects.create(
        name="test-menu",
        description="menu"
    )


@pytest.fixture
def create_dish(db, create_menu: Menu) -> Dish:
    """
    The function creates a new dish for the sample data
    """
    return Dish.objects.create(
        menu=create_menu,
        name="test dish",
        description="dish",
        price=20,
        preparation_time=30,
        is_vegetarian=False,
    )


@pytest.fixture
def create_dish_data(db) -> Callable[[str], dict[str, str]]:
    """
    The function through closure returns a function that we can call with our data
    """

    def create_clousure_dish(name: str, description: str, price: str,
                             preparation_time: str, is_vegetarian: str) -> dict[str, str]:
        return {
            "name": name,
            "description": description,
            "price": price,
            "preparation_time": preparation_time,
            "is_vegetarian": is_vegetarian,
        }

    return create_clousure_dish


@pytest.fixture
def get_new_random_dish(create_dish_data: Callable, faker: Faker) -> dict[str, str]:
    """
    The function creates a dish with random data
    """
    return create_dish_data(
        name=faker.paragraph(nb_sentences=1),
        description=faker.paragraph(nb_sentences=5),
        price=randint(1, 300),
        preparation_time=randint(5, 90),
        is_vegetarian=randint(0, 1)
    )


@pytest.fixture
def create_menu_data(db) -> Callable[[str], dict[str, str]]:
    """
    The function through closure returns a function that we can call with our data
    """

    def create_clousure_menu(name: str, description: str) -> dict[str, str]:
        return {
            "name": name,
            "description": description,
        }

    return create_clousure_menu


@pytest.fixture
def get_new_random_menu(create_menu_data: Callable, faker: Faker) -> dict[str, str]:
    """
    The function creates a menu with random data
    """
    return create_menu_data(
        name=faker.paragraph(nb_sentences=1),
        description=faker.paragraph(nb_sentences=5)
    )
