from django.core.management.base import BaseCommand
import csv
from products.models import Product
from pathlib import Path

class Command(BaseCommand):
    help = 'Import products from a CSV file located at fixtures/products_import.csv'

    def handle(self, *args, **options):
        p = Path('fixtures/products_import.csv')
        if not p.exists():
            self.stdout.write(self.style.ERROR('fixtures/products_import.csv not found'))
            return
        reader = csv.DictReader(p.read_text(encoding='utf-8').splitlines())
        created = 0
        for row in reader:
            name = row.get('name')
            if not name:
                continue
            Product.objects.create(
                name=name,
                url=row.get('url') or '',
                current_price=row.get('current_price') or 0,
                desired_price=row.get('desired_price') or 0
            )
            created += 1
        self.stdout.write(self.style.SUCCESS('Imported %d products' % created))
