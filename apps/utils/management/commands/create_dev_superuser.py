from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

import settings.local as settings


class Command(BaseCommand):
    help = 'Create test superuser, use for DEV environment only!'

    def handle(self, **_):
        User = get_user_model()
        if not User.objects.filter(username=settings.DEV_SUPERUSER_EMAIL).exists():
            User.objects.create_superuser(
                settings.DEV_SUPERUSER_EMAIL, settings.DEV_SUPERUSER_PASSWORD
            )
        self.stdout.write(self.style.SUCCESS(
            "!!! Pay attention: DEV Superuser '{username}/{pw}' is active !!!".format(
                username=settings.DEV_SUPERUSER_EMAIL, pw=settings.DEV_SUPERUSER_PASSWORD
            )
        ))
