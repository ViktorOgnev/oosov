import os
import sys
sys.path = ['/var/www/django_projects/osov'] + sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'osov.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
