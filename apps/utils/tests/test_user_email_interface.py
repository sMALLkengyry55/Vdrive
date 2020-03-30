import uuid

from django.test import TestCase

from apps.authentication.tests.factories import UserFactory
from ..user_email_interface import UserEmail


class TestUserEmailInterface(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user_email = UserEmail(self.user, uuid.uuid4())

    def test_get_user_dict(self):
        user_dict = self.user_email.get_user_dict()
        self.assertEqual(user_dict['id'], self.user.id)
        self.assertEqual(user_dict['uuid'], str(self.user_email.user_uuid))

    def test_https_check_with_http(self):
        value = 'http://'
        self.assertEqual(self.user_email._https_check(value), f'https://{value}')

    def test_https_check_with_https(self):
        value = 'https://'
        self.assertEqual(self.user_email._https_check(value), value)

    def test_create_email(self):
        email = self.user_email._create_email('auth/base_email.html')
        self.assertEqual(email.subject, self.user_email.subject)
        self.assertEqual(email.from_email, self.user_email.from_email)
        self.assertEqual(email.to, [self.user.email])
        self.assertIsNotNone(email.body)
