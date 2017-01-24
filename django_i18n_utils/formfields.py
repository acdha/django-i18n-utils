# encoding: utf-8
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from django.forms.fields import SlugField

from .validators import unicode_slug_validator


class UnicodeSlugFormField(SlugField):
    default_validators = [unicode_slug_validator]
