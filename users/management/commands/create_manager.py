from django.contrib.auth.models import Permission, Group
from django.core.management import BaseCommand

from users.models import Users


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = Users.objects.create(
            email="manager@gmail.com",
            country="Россия",
            is_staff=True,
            is_superuser=False,
        )
        user.set_password("12345")

        group = Group.objects.get(name="moderators")

        try:
            user.groups.add(group)
        except Permission.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Group {group} does not exist."))
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created/updated "moderator" with specified permissions.'
            )
        )

        user.save()
