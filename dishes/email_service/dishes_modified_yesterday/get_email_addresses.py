from general_utils.email_service.get_email_addresses_base import GetEmails
from users.models import User


class GetEmailsAllUsers(GetEmails):

    def _perform_logic(self) -> list[str]:
        """
        The function retrieves data about all authenticated users and returns their emails
        """
        return [user.email for user in User.objects.all()]
