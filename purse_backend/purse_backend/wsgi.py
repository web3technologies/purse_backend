import os

from django.core.wsgi import get_wsgi_application
from decouple import config


os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'purse_backend.settings.{config("DJANGO_SETTINGS_ENV")}')

application = get_wsgi_application()