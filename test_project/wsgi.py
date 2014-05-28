# encoding: utf-8
"""
WSGI config for test_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
from __future__ import absolute_import, print_function, unicode_literals

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_project.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()