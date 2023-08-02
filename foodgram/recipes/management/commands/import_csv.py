import csv

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Импортируем базу ингредиентов в модель'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = 'C:/Dev/foodgram-project-react/data/ingredients.csv'
        with open(path, 'rt', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                Ingredient.objects.create(
                    name=row[0],
                    measurement_unit=row[1]
                )
