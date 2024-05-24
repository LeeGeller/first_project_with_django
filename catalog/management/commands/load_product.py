import json
import pathlib

from django.core.management import BaseCommand

ROOT = pathlib.Path(__file__).parent.parent.parent.parent
DATA_PRODUCT = pathlib.Path(ROOT, 'data_for_db', 'product_data.json')


class Command(BaseCommand):
    @staticmethod
    def read_product_json_file() -> list:
        """
        Load file json from directory data_for_db
        and read it.
        :return: list with info about prducts.
        """
        with open(DATA_PRODUCT, encoding='windows-1251') as file:
            file_info = json.load(file)
        return [info for info in file_info]

    def handle(self, *args, **options):
        from catalog.models import Category
        from catalog.models import Product

        product_for_create = [
            Product
                (
                product_name=product["fields"]["product_name"],
                product_description=product["fields"]["product_description"],
                image_preview=product["fields"]["image_preview"],
                price=product["fields"]["price"],
                created_at=product["fields"]["created_at"],
                updated_at=product["fields"]["updated_at"],
                connection_with_category=Category.objects.get(
                    pk=product["fields"]["connection_with_category"])
            )

            for product in self.read_product_json_file()
        ]

        Product.objects.bulk_create(product_for_create)
