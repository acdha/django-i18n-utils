# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

import re

from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

unicode_slug_re = re.compile(r'^[-\w]+$', re.UNICODE)
unicode_slug_validator = RegexValidator(
    unicode_slug_re,
    _("Enter a valid 'slug' consisting of letters, numbers, underscores or hyphens."),
    'invalid'
)
