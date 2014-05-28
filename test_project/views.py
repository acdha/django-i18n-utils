# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

from django.http import HttpResponse
from django.utils.translation import ugettext as _


def translated_month_name(request):
    return HttpResponse(content=_('January'), content_type='text/plain; charset=utf-8')
