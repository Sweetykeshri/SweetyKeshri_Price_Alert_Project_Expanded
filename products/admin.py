from django.contrib import admin
from .models import Product, PriceHistory, PriceAlert, Watchlist, NotificationLog

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'current_price', 'desired_price', 'last_checked', 'owner')
    search_fields = ('name',)

@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'price', 'checked_at')
    list_filter = ('product',)

@admin.register(PriceAlert)
class PriceAlertAdmin(admin.ModelAdmin):
    list_display = ('product', 'email', 'triggered', 'triggered_at')
    list_filter = ('triggered',)

@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('product', 'added_at')
    filter_horizontal = ('users',)

@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ('product', 'email', 'sent_at')
    list_filter = ('sent_at',)
