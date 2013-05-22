import os
import sys
project_dir = os.path.abspath(os.path.dirname(__file__))
sys.path = [project_dir] + sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'osov.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
