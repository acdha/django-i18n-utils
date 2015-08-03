# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

import unicodedata

from django.utils import six


def clean_unicode(v):
    """
    Given an input string, return a normalized unicode string
    """

    # text_type is unicode on Python 2 and str on Python 3: https://pythonhosted.org/six/#six.text_type
    if not isinstance(v, six.text_type):
        v = six.text_type(v)

    # Normalize unicode:
    v = unicodedata.normalize("NFC", v)

    return v
