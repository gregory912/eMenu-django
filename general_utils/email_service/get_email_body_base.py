from abc import ABC, abstractmethod
from typing import Callable
from django.db.models.query import QuerySet


class GetData(ABC):
    """
    A class that manages queries to the database in order
    to obtain the appropriate data to be sent by email
    """

    @abstractmethod
    def get_data(self) -> list[QuerySet]:
        pass


class GetUrls(ABC):
    """
    The class manages the creation of URLs that can be
    sent in an email to go to a given resource
    """

    def __init__(self, data: GetData):
        self.data = data

    @abstractmethod
    def get_full_urls(self) -> list[str]:
        """
        The function returns a list of URLs
        """
        pass

    @staticmethod
    @abstractmethod
    def get_reverse(pk: str) -> str:
        """
        The function returns the full url to a given resource
        """
        pass


class GetBody(ABC):
    """
    The class prepares a body that will be sent in an e-mail
    """
    def __init__(self, urls: GetUrls, data: GetData, base_body: Callable):
        self.urls = urls.get_full_urls()
        self.data = data.get_data()
        self.base_body = base_body

    def base_email_body(self) -> Callable:
        """
        The function returns the base body code to the email
        """
        return self.base_body(self.get_full_body())

    @abstractmethod
    def get_full_body(self) -> str:
        """
        The function returns the full body for the email
        """
        pass

