import csv
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from core.models import City, Country

countries = [
    'Ukraine',
]


class Command(BaseCommand):

    help = 'Imports cities from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('--filename', help='Path to the CSV file', nargs='?', default='worldcities_tst.csv')

    def handle(self, *args, **options):
        filename = options['filename']
        # filename = 'worldcities_tst.csv'
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            with transaction.atomic():
                for row in reader:
                    # Get the country object for the city
                    country_code = row['iso2']
                    try:
                        country = Country.objects.get(code=country_code)
                    except Country.DoesNotExist:
                        raise CommandError(f'Country "{country_code}" does not exist')

                    # Create the city object
                    city = City(
                        name=row['city_ascii'],
                        country=country,
                    )
                    city.save()

        self.stdout.write(self.style.SUCCESS('Cities imported successfully'))
