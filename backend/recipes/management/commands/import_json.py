import json
import os
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from foodgram.settings import BASE_DIR
from recipes.models import Ingredient, Tag

FILE_PATH = os.path.join(
    BASE_DIR,
    'data'
)


class Command(BaseCommand):

    def handle(self, *args, **options):
        start_time = datetime.now()

        try:
            with open(
                os.path.join(FILE_PATH, 'ingredients.json')
            ) as file_json:
                data = json.load(file_json)
                for row in data:
                    Ingredient.objects.create(
                        name=row['name'],
                        measurement_unit=row['measurement_unit'],
                    )
                print('Файл ingredients.json успешно импортировал данные в БД')

            with open(
                os.path.join(FILE_PATH, 'tags.json')
            ) as file_json:
                data = json.load(file_json)
                for row in data:
                    Tag.objects.create(
                        name=row['name'],
                        color=row['color'],
                        slug=row['slug'],
                    )
                print('Файл tags.json успешно импортировал данные в БД')

        except Exception as error:
            raise CommandError(f'Произошла ошибка: {error}')

        end_time = datetime.now()
        duration = end_time - start_time
        minutes = duration.seconds // 60
        seconds = duration.seconds % 60

        self.stdout.write(
            self.style.SUCCESS(
                (f'Данные были загружены в БД за '
                 f'{minutes} минуты {seconds} секунд')
            )
        )
