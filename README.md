# Price Comparison & Alert System (Django) - Expanded

This expanded demo adds:
- Watchlist model to let users watch products (admin-managed)
- NotificationLog to store sent notifications
- Simple JSON API endpoints:
    - GET /api/products/  -> list products in JSON
    - POST /api/import-csv/ -> import CSV uploaded as form-data (key 'file')
- Management command to import CSV from fixtures/products_import.csv
- More sample products and alerts in fixtures/sample_data.json

Quick start (Linux/macOS/WSL):
1. Create and activate a virtualenv:
   python -m venv venv
   source venv/bin/activate

2. Install dependencies:
   pip install -r requirements.txt

3. Run migrations and create a superuser:
   python manage.py migrate
   python manage.py createsuperuser

4. Load sample data (optional):
   python manage.py loaddata fixtures/sample_data.json

5. Optionally import extra CSV products:
   python manage.py import_products_csv

6. Run development server:
   python manage.py runserver

7. Simulated price checks (prints emails to console and logs them):
   python manage.py run_price_checks

API examples:
- List products:
  Live Link  : http://127.0.0.1:8000/products/

- Import CSV via curl:
  curl -F "file=@fixtures/products_import.csv" http://127.0.0.1:8000/import-csv/

Notes:
- Replace simulated price fetching with real scraping/API in products.tasks.fetch_price_simulator.
- Email backend prints to console. Configure EMAIL_BACKEND in settings for real emails.
