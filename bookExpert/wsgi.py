# """
# WSGI config for bookExpert project.

# It exposes the WSGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
# """

# import os

# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookExpert.settings")

# application = get_wsgi_application()
import os
import sys
import site

# Add the app's directory to the PYTHONPATH
sys.path.append('/code/')
sys.path.append('/code/main/')
sys.path.append('/code/bookExpert/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'bookExpert.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()