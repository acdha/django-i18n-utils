# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

from django.core.exceptions import ValidationError
from django.db import models

from .utils import clean_unicode


class UnicodeNormalizerMixin(object):
    """
    Model mixin class which normalizes all text fields to NFC
    """

    def clean_fields(self, exclude=None):
        if exclude is None:
            exclude = []

        errors = {}

        try:
            super(UnicodeNormalizerMixin, self).clean_fields()
        except ValidationError as e:
            errors.update(e.message_dict)

        for field in self._meta.fields:
            if field.name in exclude:
                continue

            if not isinstance(field, (models.CharField, models.TextField)):
                continue

            v = getattr(self, field.attname)

            # Handle NULLable fields:
            if v is None:
                continue

            v = clean_unicode(v)

            # Work around a Django admin limitation where uniqueness checks are
            # performed before the blank => NULL conversion for nullable, blank
            # text fields:

            if field.null and field.blank and v == "":
                v = None

            setattr(self, field.attname, v)

        if errors:
            raise ValidationError(errors)
