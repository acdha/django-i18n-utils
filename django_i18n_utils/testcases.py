# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

from django.conf import settings
from django.test import TestCase
from django.utils import translation

from .testclients import TranslationSafeTestClient


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
                decorated_f.__name__ = str(trans_name)
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
    client_class = TranslationSafeTestClient
