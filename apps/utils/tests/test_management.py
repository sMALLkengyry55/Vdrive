from django.conf import settings
from django.test import TestCase
from django.contrib.auth import get_user_model

from ..management.commands.create_dev_superuser import Command


class TestManagement(TestCase):
    def setUp(self):
        self.User = get_user_model()

    def test_create_dev_superuser(self):
        Command().handle()  # execute 'create_dev_superuser' command from inside
        self.assertEqual(
            True,
            self.User.objects.get(email=settings.DEV_SUPERUSER_EMAIL).is_superuser
        )

    def test_not_create_if_user_exists(self):
        self.User.objects.create(
            email=settings.DEV_SUPERUSER_EMAIL,
            password=settings.DEV_SUPERUSER_PASSWORD
        )
        Command().handle()  # execute 'create_dev_superuser' command from inside
        self.assertEqual(len(self.User.objects.all()), 1)
