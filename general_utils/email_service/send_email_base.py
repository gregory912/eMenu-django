from django.core.mail import EmailMessage
from email.mime.image import MIMEImage
from pathlib import Path
from typing import Final
from abc import ABC, abstractmethod
from .get_email_body_base import GetBody
from .get_email_addresses_base import GetEmails

LOGO_PATH: Final = r"general_utils/email_service/static/restaurant.png"


class SendEmail(ABC):
    """
    The base class for sending emails
    """
    def __init__(self, body: GetBody, emails: GetEmails):
        self.paths = [LOGO_PATH]
        self.body = body.base_email_body()
        self.emails = emails.get_required_emails

    @property
    def file_paths(self) -> list[any]:
        """
        The function via property returns file paths
        """
        return self.paths

    @file_paths.setter
    def file_paths(self, new_value: list[str] | str):
        """
        The function via property adds paths to the variable
        """
        if isinstance(new_value, str):
            self.paths.append(new_value)
        elif isinstance(new_value, list):
            self.paths.extend(new_value)

    @abstractmethod
    def send_email(self) -> EmailMessage:
        """
        Send email. Add additional parameters if required
        """
        return self._get_obj()

    @abstractmethod
    def _get_obj(self):
        """
        Returns an email object with appropriate parameters
        """
        pass

    @staticmethod
    def _add_header_with_file(path: str) -> MIMEImage:
        """
        The function returns a header object that can be sent via email
        """
        with open(path, mode='rb') as f:
            image = MIMEImage(f.read())
            image.add_header('Content-ID', f"<{Path(path).name}>")
            return image
