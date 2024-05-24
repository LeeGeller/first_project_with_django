from django.contrib.auth.models import User, Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Создание группы модераторов
        group = Group.objects.create(name="moderators")

        permissions_codenames = [
            "cancel_product",
            "change_product_description",
            "add_versionproduct",
        ]

        for permission in permissions_codenames:
            try:
                permissions = Permission.objects.get(codename=permission)
                group.permissions.add(permissions)
            except Permission.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"Permission {permission} does not exist.")
                )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created/updated group "moderators" with specified permissions.'
                )
            )
