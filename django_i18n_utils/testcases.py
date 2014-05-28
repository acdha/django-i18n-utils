# encoding: utf-8
from __future__ import absolute_import

from django.conf import settings
from django.test import TestCase
from django.test.client import Client as TestClient
from django.utils import translation


class TranslationSafeClient(TestClient):
    """TestClient subclass which preserves the active language

    Django's LocaleMiddleware deactivates the current language at the end
    of each request, which resets it to the default. This is fine in normal
    operation but annoying if your unit tests want to confirm that translated
    text was present in the response as _(foo) will return the system default
    language if you call it after making a request using the test client
    """

    def request(self, *args, **kwargs):
        active_lang = translation.get_language()

        if active_lang is not None:
            kwargs['HTTP_ACCEPT_LANGUAGE'] = active_lang

        try:
            return super(TranslationSafeClient, self).request(*args, **kwargs)
        finally:
            translation.activate(active_lang)


class LocalizedTestCaseMetaclass(type):
    """Replace _localized methods with per-language wrappers

    See description in :class:`LocalizedTestCase`
    """

    def __new__(meta, class_name, base_classes, class_dict):
        for method_name, method in class_dict.items():
            if not (method_name.startswith("test")
                    and method_name.endswith("localized")):
                continue

            class_dict.pop(method_name)

            for lang, name in settings.LANGUAGES:
                trans_name = '%s_%s' % (method_name, lang)
                decorated_f = meta.activate_language(lang, method)
                # nose magic: see http://stackoverflow.com/questions/5176396/
                decorated_f.__name__ = trans_name
                class_dict[trans_name] = decorated_f

        return type.__new__(meta, class_name, base_classes, class_dict)

    @staticmethod
    def activate_language(lang, method):
        def inner(self, *args, **kwargs):
            with translation.override(lang):
                self.active_language = lang

                try:
                    return method(self, *args, **kwargs)
                finally:
                    del self.active_language

        return inner


class LocalizedTestCase(TestCase):
    """multi-lingual testcase helper

    This uses :class:`LocalizedTestCaseMetaclass` to replace any test method
    whose name ends in localized with one copy for each language in
    settings.LANGUAGES: e.g. `test_foo` will be replaced with (`test_foo_ar`,
    `test_foo_en`, …)

    When the test method is called, the correct language will be activated and
    the test client will set the HTTP Accept-Language header as expected. For
    convenience, self.active_language will be set appropriately
    """

    __metaclass__ = LocalizedTestCaseMetaclass

    #: We need our custom TestClient subclass to ensure that the correct
    #: translation is activated:
    client_class = TranslationSafeClient
