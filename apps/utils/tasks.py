import uuid

from urllib.parse import urlencode

from django.conf import settings
from django.core.cache import cache
from django.utils.translation import ugettext as _

from celery import shared_task

from .communication import encode_dict_to_base64
from .user_email_interface import UserEmail


class UserConfirmationEmail(UserEmail):

    def __init__(self, *args, **kwargs):
        super(UserConfirmationEmail, self).__init__(*args, **kwargs)
        self.subject = settings.EMAIL_SUBJECT_PATTERN % _('email confirmation')

    def cache_result(self):
        cache.set(f'email_confirmation_{self.user.id}', self.get_user_dict(), timeout=3600*12)

    def send(self):
        # relative url for client side to verify user account
        self.cache_result()
        hash_value = urlencode({'hash': encode_dict_to_base64(self.get_user_dict())})
        extra_context = {'email_confirmation_link': f'/api/v1/auth/confirm_email/?{hash_value}'}
        email = self.create_html_email(
            template='auth/email_confirmation.html',
            extra_context=extra_context
        )
        self.send_email(email)


class UserPasswordRestoreEmail(UserEmail):

    def __init__(self, *args, **kwargs):
        super(UserPasswordRestoreEmail, self).__init__(*args, **kwargs)
        self.subject = settings.EMAIL_SUBJECT_PATTERN % _('restore password')

    def cache_result(self):
        cache.set(f'password_restore_{self.user.id}', self.get_user_dict(), timeout=3600)

    def send(self):
        self.cache_result()
        # TODO generate restore link with right host
        hash_value = urlencode({'hash': encode_dict_to_base64(self.get_user_dict())})
        extra_context = {'restore_password_link': f'/api/v1/auth/restore_password/?{hash_value}'}
        email = self.create_html_email(
            template='auth/restore_password.html',
            extra_context=extra_context,
        )
        self.send_email(email)


class UserCreatedNotificationEmail(UserEmail):

    def __init__(self, *args, **kwargs):
        super(UserCreatedNotificationEmail, self).__init__(*args, **kwargs)
        self.subject = settings.EMAIL_SUBJECT_PATTERN % _('registration completed')

    def send(self):
        email = self.create_html_email(
            template='auth/success_registration.html'
        )
        self.send_email(email)


# Celery tasks
def _send_email(user_id, email_class):
    if not issubclass(email_class, UserEmail):
        raise TypeError('"email_class" argument must be a subclass of UserEmail')
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = User.objects.get(id=user_id)
    user_email = email_class(user=user, uuid=uuid.uuid4())
    user_email.send()


@shared_task
def send_email_confirmation_link(user_id):
    _send_email(user_id, UserConfirmationEmail)


@shared_task
def send_password_restore_link(user_id):
    _send_email(user_id, UserPasswordRestoreEmail)


@shared_task
def send_notification_user_created(user_id):
    _send_email(user_id, UserCreatedNotificationEmail)
