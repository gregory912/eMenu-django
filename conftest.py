import pytest
from rest_framework.test import APIClient
from faker import Faker
from typing import Callable


@pytest.fixture
def api_client() -> APIClient:
    """
    The function returns APIClient object
    """
    return APIClient()


@pytest.fixture
def faker() -> Faker:
    """
    The function returns Faker object
    """
    return Faker()


@pytest.fixture
def create_user_data(db) -> Callable[[str], dict[str, str]]:
    """
    The function through closure returns a function that we can call with our data
    """
    def create_app_user(username: str, password: str, first_name: str, last_name: str, email: str,
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

    return create_app_user


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
