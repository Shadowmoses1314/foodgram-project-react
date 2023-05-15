import csv
import json
import logging
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from recipes.models import Recipe

logging.basicConfig(
    level=logging.INFO,
    filename='main.log',
    format='%(asctime)s, %(levelname)s, %(name)s, %(message)s',
    filemode='w',
)

DATA_ROOT = os.path.join(settings.BASE_DIR, 'data')


class Command(BaseCommand):
    help = 'Load data from csv file into the database'

    def add_arguments(self, parser):
        parser.add_argument('filename', default='recipes.csv', nargs='?',
                            type=str)

    def handle(self, *args, **options):
        try:
            with open(
                os.path.join(DATA_ROOT, options['filename']),
                newline='',
                encoding='utf8'
            ) as csv_file:
                data = csv.reader(csv_file)
                for row in data:
                    (
                        name,
                        author,
                        image,
                        text,
                        tags, ingredients, cooking_time) = row
                    ingredients = json.dumps(
                        ingredients)
                    Recipe.objects.get_or_create(
                        name=name,
                        author=author,
                        text=text,
                        image=image,
                        cooking_time=cooking_time,
                        tags=tags,
                        ingredients=ingredients
                    )
        except FileNotFoundError:
            raise CommandError('Добавьте файл recipes в директорию data')
