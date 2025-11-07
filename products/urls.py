from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('products/', views.product_list, name='list'),
    path('products/<int:pk>/', views.product_detail, name='detail'),
    path('products/<int:pk>/check/', views.manual_check, name='manual_check'),
    path('api/products/', views.api_products, name='api_products'),
    path('api/import-csv/', views.api_import_csv, name='api_import_csv'),
]
