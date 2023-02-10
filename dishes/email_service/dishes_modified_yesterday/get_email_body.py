from django.urls import reverse
from django.utils.timezone import make_aware
from dishes.models import Dish
from general_utils.email_service.get_email_body_base import GetData, GetBody, GetUrls
from general_utils.email_service.send_email_base import LOGO_PATH
from datetime import datetime, timedelta, time, date
from typing import Any
import os


class GetDataDishesModifiedYesterday(GetData):

    def get_data(self) -> dict[str, Any]:
        """
        The function retrieves all dishes that were modified yesterday
        """
        return {
            "created": self.get_created_dishes(),
            "modified": self.get_modified_dishes()
        }

    def get_modified_dishes(self) -> Dish:
        """
        The function returns all dishes that were modified yesterday but were created earlier
        """
        return Dish.objects.filter(
            modified__gt=self._get_start_date(),
            modified__lt=self._get_end_date(),
            created__lt=self._get_start_date(),
        )

    def get_created_dishes(self) -> Dish:
        """
        The function returns all the dishes that were created yesterday
        """
        return Dish.objects.filter(
            created__gt=self._get_start_date(),
            created__lt=self._get_end_date(),
        )

    def _get_start_date(self) -> datetime:
        """
        The function returns the date of the previous day in the format 2023-01-01 00:00:00
        """
        return self._get_aware_base_date(datetime.utcnow().date()) - timedelta(days=1)

    def _get_end_date(self) -> datetime:
        """
        The function returns today's date in the format 2023-01-01 00:00:00
        """
        return self._get_aware_base_date(datetime.utcnow().date())

    @staticmethod
    def _get_aware_base_date(date_: date) -> datetime:
        """
        The function based on the date creates an aware datetime in the format 2023-01-01 00:00:00
        """
        return make_aware(datetime.combine(date_, time()))


class GetUrlsDishesModifiedYesterday(GetUrls):

    def get_full_urls(self) -> dict[str, list[str]]:
        """
        The function returns a list of URLs to dishes
        """
        data = self.data.get_data()
        return {
            "created": [self.get_reverse(item.id) for item in data["created"]],
            "modified": [self.get_reverse(item.id) for item in data["modified"]],
        }

    @staticmethod
    def get_reverse(pk: str) -> str:
        """
        The function returns the full URL to the dish
        """
        return fr"http://127.0.0.1:8000{reverse('dish_detail', args=[pk])}"


class GetBodyDishesModifiedYesterday(GetBody):

    def get_full_body(self) -> str:
        """
        The function returns full body that can be sent via email
        """
        urls = self.urls.get_full_urls()
        data = self.data.get_data()
        return f"""
            <body>
            <div class="main">
                <div class="logo-con">
                    <div class="logo">
                        <img alt="" class="img-job" src='cid:{self.get_logo_file_name()}'/>
                    </div>
                </div>
                
                <div class="text-con">
                <div class="title">
                    <h2>Check out our latest recipes!</h2>
                </div>
                
                {'<h3 class="title_content">See our latest recipes!</h3>' if data['created'] else ''}
                {self.get_dynamic_content(urls['created'], data['created'])}
                
                {'<h3 class="title_content">See our recently modified recipes!</h3>' if data['modified'] else ''}
                {self.get_dynamic_content(urls['modified'], data['modified'])}
                
                {self.get_footer()}
                    
                </div>
            </div>
            <footer>
            </footer>
            </body>
            """

    @staticmethod
    def get_dynamic_content(urls, data) -> str:
        """
        The function returns dynamically created content
        """
        body_content = ''
        for counter, (url, item) in enumerate(zip(urls, data)):

            body_content += f"""
            <div class="content">
                    <h3>{item.name}</h3>
                    <div class="btn-con">
                            <a target="_blank" class="btn" href="{url}"><p class="color-button">Click</p></a>
                    </div>
                </div>
            """
            if counter == 1:
                return body_content
        return body_content

    @staticmethod
    def get_footer() -> str:
        """
        Return the footer at the very bottom of the email
        """
        return f"""
            <div class="content">
                <h3>If you want to see more recently added recipes, visit our website!</h3>
            </div>
            """

    @staticmethod
    def get_logo_file_name() -> str:
        """
        The path function returns information about the file
        """
        return os.path.basename(LOGO_PATH)
