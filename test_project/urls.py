# encoding: utf-8
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns

from .views import translated_month_name

urlpatterns = i18n_patterns(
    url(r'^month-name/$', translated_month_name, name='translated-month-name'),
)
