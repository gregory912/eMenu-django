from abc import ABC, abstractmethod


class GetEmails(ABC):
    """
    The class manages the filtering of emails that
    meet a given condition to be sent to them by email
    """

    @property
    def get_required_emails(self) -> list[str]:
        """
        The function returns all emails that meet the conditions
        """
        return self._perform_logic()

    @abstractmethod
    def _perform_logic(self) -> list[str]:
        """
        The function performs all required operations in order to receive correct e-mails
        """
        pass
