# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

import unicodedata

from django.utils.encoding import force_unicode


def clean_unicode(v):
    """
    Given an input string, return a normalized unicode string
    """

    if not isinstance(v, unicode):
        v = force_unicode(v)

    # Normalize unicode:
    v = unicodedata.normalize("NFC", v)

    return v
