# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns

urlpatterns = i18n_patterns('',
    url(r'^month-name/$', 'test_project.views.translated_month_name', name='translated-month-name'),
)
