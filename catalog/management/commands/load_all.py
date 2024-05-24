import json
import pathlib

from django.core.management import BaseCommand

from blog.models import BlogPost

ROOT = pathlib.Path(__file__).parent.parent.parent.parent
DATA_PRODUCT = pathlib.Path(ROOT, "data_for_db", "posts.json")


class Command(BaseCommand):
    @staticmethod
    def read_product_json_file() -> list:
        """
        Load file json from directory data_for_db
        and read it.
        :return: list with info about products.
        """
        with open(DATA_PRODUCT, encoding="utf-8") as file:
            file_info = json.load(file)
        return [info for info in file_info]

    def handle(self, *args, **options):

        product_for_create = [
            BlogPost(
                title=product["fields"]["title"],
                text_area=product["fields"]["text_area"],
            )
            for product in self.read_product_json_file()
        ]

        BlogPost.objects.bulk_create(product_for_create)
