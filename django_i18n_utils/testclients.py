# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

from django.test.client import Client
from django.utils import translation


class TranslationSafeTestClient(Client):
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
            return super(TranslationSafeTestClient, self).request(*args, **kwargs)
        finally:
            translation.activate(active_lang)
