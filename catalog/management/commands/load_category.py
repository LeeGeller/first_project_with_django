import json
import pathlib

from django.core.management import BaseCommand

ROOT = pathlib.Path(__file__).parent.parent.parent.parent
DATA_CATEGORY = pathlib.Path(ROOT, 'data_for_db', 'category_data.json')


class Command(BaseCommand):
    @staticmethod
    def read_category_json_file() -> list:
        """
        Load file json from directory data_for_db
        and read it.
        :return: list with info about categories.
        """
        with open(DATA_CATEGORY, encoding='utf-8') as file:
            file_info = json.load(file)
        return [info for info in file_info]

    def handle(self, *args, **options):
        from catalog.models import Category

        category_for_create = [
            Category
                (
                category_name=category["fields"]["category_name"],
                category_description=category["fields"]["category_description"]
            )
            for category in self.read_category_json_file()
        ]

        Category.objects.bulk_create(category_for_create)
