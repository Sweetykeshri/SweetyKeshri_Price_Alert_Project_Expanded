import random
from decimal import Decimal
from django.utils import timezone
from django.core.mail import send_mail
from .models import Product, PriceHistory, PriceAlert, NotificationLog

def fetch_price_simulator(product):
    # Simulate getting price from web by random walk around current_price
    base = float(product.current_price)
    delta = random.uniform(-0.15, 0.15) * base
    new_price = max(1.0, base + delta)
    return Decimal(str(round(new_price, 2)))

def simulate_price_check_for_product(product_id):
    product = Product.objects.get(pk=product_id)
    new_price = fetch_price_simulator(product)
    # Save history
    PriceHistory.objects.create(product=product, price=new_price)
    product.current_price = new_price
    product.last_checked = timezone.now()
    product.save()

    # Check alerts
    alerts = PriceAlert.objects.filter(product=product, triggered=False)
    for a in alerts:
        if new_price <= a.product.desired_price:
            a.triggered = True
            a.triggered_at = timezone.now()
            a.save()
            # send email (console backend in settings prints this)
            subject = f'Price Alert: {product.name} is now ₹{new_price}'
            message = f'The product {product.name} has reached your target price (₹{a.product.desired_price}). Current price: ₹{new_price}. URL: {product.url or "N/A"}'
            send_mail(subject, message, 'alerts@example.com', [a.email])
            # log notification
            NotificationLog.objects.create(product=product, email=a.email, subject=subject, message=message)
