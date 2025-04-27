import os
from django.core.wsgi import get_wsgi_application

# Set the default settings module for the 'django' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_tracker_backend.settings')

# Create an application object that can be used by WSGI servers (like Gunicorn).
application = get_wsgi_application()
