"""
WSGI config for bcloud project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""
import os
import sys
import uwsgi
from uwsgidecorators import timer
from django.utils import autoreload

sys.path.append('/home/bcloud/ENV')
sys.path.append('/home/bcloud/preprod/bcloud')
sys.path.append('/home/bcloud/preprod/bcloud/bcloud')

os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bcloud.settings")

from django.core.wsgi import get_wsgi_application
import django.core.handlers.wsgi
application = get_wsgi_application()
application = django.core.handlers.wsgi.WSGIHandler()

@timer(3)
def change_code_gracefull_reload(sig):
    if autoreload.code_changed():
        uwsgi.reload()
