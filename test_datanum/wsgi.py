"""
WSGI config for test_datanum project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/home/scott/ws/py/django_projects/test_datanum/test_datanum')
sys.path.append('/home/scott/ws/py/django_projects/test_datanum')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_datanum.settings')

application = get_wsgi_application()
