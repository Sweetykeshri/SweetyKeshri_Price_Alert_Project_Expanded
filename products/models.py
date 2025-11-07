from django.db import models
from django.contrib.auth import get_user_model

class Product(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(blank=True, null=True)
    desired_price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Alert when current_price <= desired_price')
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    last_checked = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='products')

    def __str__(self):
        return f'{self.name} - ₹{self.current_price}'

class PriceHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='history')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    checked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-checked_at']

class PriceAlert(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='alerts')
    email = models.EmailField()
    triggered = models.BooleanField(default=False)
    triggered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Alert for {self.product.name} -> {self.email}'

class Watchlist(models.Model):
    users = models.ManyToManyField(get_user_model(), related_name='watchlists')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='watchlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product',)

    def __str__(self):
        return f'Watchlist entry for {self.product.name}'

class NotificationLog(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sent_at']
