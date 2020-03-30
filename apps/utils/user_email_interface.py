from django.conf import settings
from django.core import mail
from django.template.loader import render_to_string

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


# TODO: refactor to implement correct solid components.
class UserEmail:
    """
    A simple interface to manipulate User email sending and follow DRY.
    TODO: recheck everything
    """

    def __init__(self, user, uuid, *args, **kwargs):
        self.user = user
        self.user_uuid = uuid
        self.from_email = settings.DEFAULT_FROM_EMAIL
        self.subject = settings.EMAIL_SUBJECT_PATTERN % 'Email Notification'

    def get_user_dict(self):
        return {'id': self.user.id, 'uuid': str(self.user_uuid)}

    def _https_check(self, value):
        """
        Simple https check. Add it if there is no such protocal here.
        Suitable for email specifically.
        """
        if not value.startswith('https'):
            return f'https://{value}'
        return value

    def get_general_context(self):
        """
        Provide default context like os environment variables
        """
        site_host = self._https_check(settings.FRONT_HOST)
        logger.debug(f'CLIENT HOST is {site_host}')

        api_host = self._https_check(settings.STATIC_HOST)
        logger.debug(f'API HOST is {api_host}')

        return {
            'site_host': site_host,
            'api_host': api_host,
            'user': self.user
        }

    def _create_email(self, template, **kwargs):
        context = self.get_general_context()
        extra_context = kwargs.get('extra_context', None)
        if extra_context:
            context = {**context, **extra_context}
        body = render_to_string(
            template,
            context=context
        )
        email = mail.EmailMultiAlternatives(
            subject=self.subject,
            body=body,
            from_email=self.from_email,
            to=[self.user.email]
        )
        return email

    def create_html_email(self, template, *args, **kwargs):
        email = self._create_email(template, *args, **kwargs)
        email.attach_alternative(email.body, 'text/html')
        return email

    def send_email(self, email):
        sent_count = email.send()
        logger.info(f'{sent_count} Email ({email.subject}) was sent to {email.to}')

    def send(self):
        raise NotImplementedError()
