from dishes.email_service.dishes_modified_yesterday.get_email_body import GetBodyDishesModifiedYesterday, \
    GetDataDishesModifiedYesterday, GetUrlsDishesModifiedYesterday
from dishes.email_service.dishes_modified_yesterday.get_email_addresses import GetEmailsAllUsers
from dishes.email_service.dishes_modified_yesterday.send_email import SendEmailDishesModifiedYesterday
from general_utils.email_service.email_base_form import base_email_form


def send_email_dishes_modified_yesterday() -> None:
    """
    The function manages the downloading of all dishes added or
    modified yesterday and sending them to all users
    """
    dishes_data_obj = GetDataDishesModifiedYesterday()

    dishes_data = dishes_data_obj.get_data()

    if dishes_data['created'] or dishes_data['modified']:

        dishes_body_obj = GetBodyDishesModifiedYesterday(
            GetUrlsDishesModifiedYesterday(dishes_data_obj),
            dishes_data_obj,
            base_email_form
        )

        emails_obj = GetEmailsAllUsers()

        send_email_instance = SendEmailDishesModifiedYesterday(
            dishes_body_obj,
            emails_obj
        )

        send_email_instance.send_email()
