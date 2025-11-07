from django.core.management.base import BaseCommand
from products.models import Product
from products.tasks import simulate_price_check_for_product

class Command(BaseCommand):
    help = 'Simulate checking prices for all products and send alerts (prints emails to console).'

    def handle(self, *args, **options):
        products = Product.objects.all()
        for p in products:
            simulate_price_check_for_product(p.pk)
        self.stdout.write(self.style.SUCCESS('Done simulated price checks for %d products' % products.count()))
