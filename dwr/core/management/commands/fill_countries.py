from django.core.management import BaseCommand

import pycountry
from django.db import transaction

from core.models import Country


class Command(BaseCommand):
    def handle(self, *args, **options):
        with transaction.atomic():
            for country in pycountry.countries:
                if not Country.objects.filter(code=country.alpha_2).exists():
                    Country.objects.create(
                        name=country.name,
                        code=country.alpha_2
                    )
