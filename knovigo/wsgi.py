from dotenv import load_dotenv
from pathlib import Path
env_path = Path('..') / 'knovigo-dev.env'
load_dotenv(dotenv_path=env_path)

"""
WSGI config for knovigo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'knovigo.settings')

application = get_wsgi_application()
