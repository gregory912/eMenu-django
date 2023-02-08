from general_utils.email_service.send_email_base import SendEmail
from django.core.mail import EmailMultiAlternatives


class SendEmailDishesModifiedYesterday(SendEmail):

    def send_email(self):
        email = super().send_email()
        email.send()

    def _get_obj(self) -> EmailMultiAlternatives:
        email = EmailMultiAlternatives(
            subject=f'Check out the latest dishes!',
            to=self.emails
        )
        email.content_subtype = 'html'
        email.attach_alternative(self.body, "text/html")
        email.mixed_subtype = 'related'
        email.attach(self._add_header_with_file(self.paths[0]))
        return email

