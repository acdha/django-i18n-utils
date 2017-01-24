# encoding: utf-8


from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns

from .views import translated_month_name

urlpatterns = i18n_patterns('',
    url(r'^month-name/$', translated_month_name, name='translated-month-name'),
)
