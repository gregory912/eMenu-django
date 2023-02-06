import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.exceptions import ErrorDetail
from users.models import User
from typing import Callable


@pytest.mark.django_db
def test_user_creation_for_correct_data(api_client: APIClient, get_new_random_user: dict[str, str]):
    """
    Test that the function creates and saves the user to the database
    """
    url = reverse('auth_register')

    data = get_new_random_user
    response = api_client.post(url, data=data)

    assert response.status_code == 201
    assert User.objects.filter(email=data['email']).exists()


@pytest.mark.django_db
def test_user_creation_for_incorrect_email(
        api_client: APIClient,
        create_user_data: Callable[[str], dict[str, str]]):
    """
    Testing whether an error will be returned for an incorrectly entered e-mail
    """
    url = reverse('auth_register')

    data = create_user_data("john", "example_password", "John", "Doe", "test.johngmail.com")
    response = api_client.post(url, data=data)

    assert response.status_code == 400


@pytest.mark.django_db
def test_user_creation_for_incorrect_password_confirmation(
        api_client: APIClient,
        create_user_data: Callable[[str], dict[str, str]]):
    """
    Testing whether an error will be returned for an incorrectly entered password confirmation
    """
    url = reverse('auth_register')

    data = create_user_data("john", "example_password", "John", "Doe", "test.john@gmail.com")
    data['password_confirmation'] = 'test_password'
    response = api_client.post(url, data=data)

    assert response.status_code == 400
    assert isinstance(response.data['password'][0], ErrorDetail)


@pytest.mark.django_db
def test_user_creation_without_required_fields(api_client: APIClient):
    """
    Testing whether an error will be returned for missing required data
    """
    url = reverse('auth_register')

    data = {}
    response = api_client.post(url, data=data)

    fields = ['username', 'first_name', 'password', 'password_confirmation', 'last_name', 'email']

    assert response.status_code == 400
    assert all([True if isinstance(response.data[x][0], ErrorDetail) else False for x in fields])
