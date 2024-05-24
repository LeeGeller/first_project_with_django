import os

from django.core.management import BaseCommand

from users.models import Users

PASSWORD = os.getenv("pass_user")


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = Users.objects.create(
            email="admin@gmail.com",
            country="Россия",
            is_staff=True,
            is_superuser=True,
        )

        user.set_password("12345")
        user.save()
