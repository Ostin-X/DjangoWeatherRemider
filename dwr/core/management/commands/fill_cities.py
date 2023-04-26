import csv
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from core.models import City, Country

countries = [
    'Ukraine',
    'Spain',
    'Italy',
    'France',
    'Germany',
    'Poland',
    'United Kingdom',
    "United States",
]


class Command(BaseCommand):
    help = 'Imports cities from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('--filename', help='Path to the CSV file', nargs='?', default='worldcities.csv')

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

                    if (row['population'] and float(row['population']) > 1000000 or
                        row['capital'] and row['capital'] == 'primary' and row['population'] and float(row['population']) > 100000 or
                        row['country'] == 'Ukraine' and float(row['population']) > 500000) and row['country'] in countries\
                        or row['city'] == 'Las Palmas':

                        print(row['city'], row['country'], row['population'])
                        # Create the city object
                        if not City.objects.filter(name=row['city'], country=country).exists():
                            city = City(
                                name=row['city'],
                                country=country,
                            )
                            city.save()

        self.stdout.write(self.style.SUCCESS('Cities imported successfully'))
