from django.db.models.query import QuerySet
from django.urls import reverse
from dishes.models import Dish
from general_utils.email_service.get_email_body_base import GetData, GetBody, GetUrls
from general_utils.email_service.send_email_base import LOGO_PATH
from datetime import date, timedelta
import os


class GetDataDishesModifiedYesterday(GetData):

    def get_data(self) -> list[QuerySet]:
        """
        The function retrieves all dishes that were modified yesterday
        """
        return Dish.objects.filter(
            modified__gt=self._get_day_before_yesterday_date(),
            modified__lt=date.today(),
        )

    @staticmethod
    def _get_day_before_yesterday_date() -> date:
        """
        Return date from the day before yesterday
        """
        return date.today() - timedelta(days=2)


class GetUrlsDishesModifiedYesterday(GetUrls):

    def get_full_urls(self) -> list[str]:
        """
        The function returns a list of URLs to dishes
        """
        return [self.get_reverse(item.id) for item in self.data.get_data()]

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
                
                {self.get_dynamic_content()}
                    
                </div>
            </div>
            <footer>
            </footer>
            </body>
            """

    def get_dynamic_content(self) -> str:
        """
        The function returns dynamically created content
        """
        body_content = ''
        for counter, (url, data) in enumerate(zip(self.urls, self.data)):

            body_content += f"""
            <div class="content">
                    <h3>{data.name}</h3>
                    <div class="btn-con">
                            <a target="_blank" class="btn" href="{url}"><p class="color-button">Click</p></a>
                    </div>
                </div>
            """
            if counter == 4:
                body_content += f"""
                            <div class="content">
                                    <h3>If you want to see more recently added recipes, visit our website!</h3>
                            </div>
                            """
                return body_content
        return body_content

    @staticmethod
    def get_logo_file_name() -> str:
        """
        The path function returns information about the file
        """
        return os.path.basename(LOGO_PATH)
