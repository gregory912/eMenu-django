import pytest
from dishes.email_service.dishes_modified_yesterday.get_email_addresses import GetEmailsAllUsers
from dishes.email_service.dishes_modified_yesterday.get_email_body import GetDataDishesModifiedYesterday
from menus.models import Menu
from users.models import User
from dishes.models import Dish
from datetime import datetime, timedelta


def test_get_emails_of_all_users(create_user: User):
    """
    Test if the get_required_emails function returns the correct number of emails
    """
    assert User.objects.all().count() == len(GetEmailsAllUsers().get_required_emails)


def test_dishes_modified_yesterday_correct_date(mocker, get_new_random_dish: dict[str, str], create_menu: Menu):
    """
    Test if the function GetDate Dishes Modified Yesterday returns all dishes from yesterday
    Functions in Django were mocked for testing purposes
    """
    patcher = mocker.patch("django.utils.timezone.now", return_value=datetime.today() - timedelta(days=1))
    Dish.objects.create(menu=create_menu, **get_new_random_dish)

    assert Dish.objects.all().count() == len(GetDataDishesModifiedYesterday().get_data())
    patcher.stop()


def test_dishes_modified_yesterday_today_date(mocker, get_new_random_dish: dict[str, str], create_menu: Menu):
    """
    Verify that GetDate Dishes Modified Yesterday does not return data
    for an incorrectly entered value for today
    Functions in Django were mocked for testing purposes
    """
    patcher = mocker.patch("django.utils.timezone.now", return_value=datetime.today())
    Dish.objects.create(menu=create_menu, **get_new_random_dish)

    assert len(GetDataDishesModifiedYesterday().get_data()) == 0
    patcher.stop()


def test_dishes_modified_yesterday_day_before_yesterday(mocker, get_new_random_dish: dict[str, str], create_menu: Menu):
    """
    Verify that GetDate Dishes Modified Yesterday does not return data
    for an incorrectly entered value for day before yesterday
    Functions in Django were mocked for testing purposes
    """
    patcher = mocker.patch("django.utils.timezone.now", return_value=datetime.today() - timedelta(days=2))
    Dish.objects.create(menu=create_menu, **get_new_random_dish)

    assert len(GetDataDishesModifiedYesterday().get_data()) == 0
    patcher.stop()
