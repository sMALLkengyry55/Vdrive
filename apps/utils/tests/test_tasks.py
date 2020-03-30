from django.conf import settings
from django.core import mail
from django.test import TestCase

from apps.authentication.tests.factories import UserFactory
from ..tasks import send_notification_user_created, send_password_restore_link


class TestSendEmailWithAttachment(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_send_password_restore_link(self):
        send_password_restore_link(self.user.id)
        sent_email = mail.outbox[0]
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(sent_email.subject, settings.EMAIL_SUBJECT_PATTERN % 'restore password')
        self.assertEqual(sent_email.from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(sent_email.to[0], self.user.email)

    def send_notification_user_created(self):
        send_notification_user_created(self.user.id)
        sent_email = mail.outbox[0]
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(sent_email.subject, settings.EMAIL_SUBJECT_PATTERN % 'registration completed')
        self.assertEqual(sent_email.from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(sent_email.to[0], self.user.email)
