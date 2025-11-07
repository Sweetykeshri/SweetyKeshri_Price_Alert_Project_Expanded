from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, PriceHistory, NotificationLog
from django.contrib import messages
from django.utils import timezone
from .tasks import simulate_price_check_for_product
from django.http import JsonResponse, HttpResponseBadRequest
import csv, io
from django.views.decorators.http import require_http_methods

def product_list(request):
    products = Product.objects.all().order_by('name')
    return render(request, 'products/list.html', {'products': products})

def product_detail(request, pk):
    p = get_object_or_404(Product, pk=pk)
    return render(request, 'products/detail.html', {'product': p})

def manual_check(request, pk):
    p = get_object_or_404(Product, pk=pk)
    simulate_price_check_for_product(p.pk)
    messages.success(request, 'Manual price check simulated (check console for email alerts).')
    return redirect('products:detail', pk=pk)

def api_products(request):
    products = Product.objects.all().values('id','name','current_price','desired_price','url','last_checked')
    return JsonResponse({'products': list(products)})

@require_http_methods(["POST"])
def api_import_csv(request):
    # Accepts a CSV file upload (fields: name,url,current_price,desired_price)
    f = request.FILES.get('file')
    if not f:
        return HttpResponseBadRequest('No file uploaded. Send as form-data with key "file".')
    data = f.read().decode('utf-8')
    reader = csv.DictReader(io.StringIO(data))
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
    return JsonResponse({'created': created})

