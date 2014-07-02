# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

from functools import update_wrapper

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.fields import SlugField

from .formfields import UnicodeSlugFormField
from .utils import clean_unicode
from .validators import unicode_slug_validator


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


def unicode_safe_repr(format_string, field_names):
    """Class decorator which ensures that repr will return a Unicode-escaped safe for ASCII consumers

    Requires a format string and a list of class attributes to be included for formatting. All strings will
    be encoded using the `unicode_escape` encoding. Values which have a `pk` attribute – e.g. Django models –
    will be processed using `repr()` so this must be applied to all of your foreign-key classes as well.

    Usage::

        @unicode_safe_repr(u'{class_name}(title=u"{title}")', ('title', ))
        class MyDjangoModel(…):
            …
    """

    assert isinstance(format_string, unicode), 'format_string must be Unicode!'

    def inner(cls):
        def safe_repr(self):
            field_values = []

            for k in field_names:
                v = getattr(self, k)

                if hasattr(v, 'pk'):
                    field_values.append(repr(v))
                elif isinstance(v, basestring):
                    field_values.append(v.encode('unicode_escape'))
                else:
                    field_values.append(v)

            values = {'class_name': cls.__name__}
            values.update(zip(field_names, field_values))
            return format_string.format(**values)

        update_wrapper(safe_repr, cls.__repr__)
        cls.__repr__ = safe_repr

        return cls

    return inner


class UnicodeSlugField(SlugField):
    default_validators = [unicode_slug_validator]

    def formfield(self, **kwargs):
        defaults = {'form_class': UnicodeSlugFormField}
        defaults.update(kwargs)
        return super(UnicodeSlugField, self).formfield(**defaults)
