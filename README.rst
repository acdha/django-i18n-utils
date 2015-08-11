=================================
Django Internationalization Utils
=================================

.. image:: https://travis-ci.org/acdha/django-i18n-utils.svg?branch=master
    :target: https://travis-ci.org/acdha/django-i18n-utils


Data Processing
~~~~~~~~~~~~~~~

clean_unicode
-------------

`utils.clean_unicode` accepts an input string and returns
normalized Unicode

UnicodeNormalizerMixin
----------------------

Model mixin class which ensures that every text field has been processed with
`clean_unicode` during model validation's `clean_fields` step

Testing
~~~~~~~

TranslationSafeTestClient
-------------------------

Django `TestClient` subclass which resets the active translation after each request to avoid leaking
translation state across tests, causing hard-to-debug side-effects like loading fixtures in the wrong
language using `django-modeltranslation <https://pypi.python.org/pypi/django-modeltranslation>`_.

Usage::

    from django_i18n_utils.testclients import TranslationSafeTestClient

    class MyTestCase(TestCase):
        client_class = TranslationSafeTestClient

        def test_foo(self):
            # default language active
            self.client.get('/pt/myview') # Portuguese active when the view executes
            # default language active again


TranslationSafeTestCase
-----------------------

Django `TestCase` subclass which uses `TranslationSafeTestClient` to avoid test failures caused by previous
tests leaving an unexpected locale active.

Usage::

    from django_i18n_utils.testcases import TranslationSafeTestCase

    class MyTestCase(TranslationSafeTestCase):
        …


LocalizedTestCase
-----------------

Django `TestCase` subclass which makes it easy to create per-language tests
without duplication or for-loops::

    class MyLocalizedTests(LocalizedTestCase):
        def test_homepage(self):
            …

will execute and display as if you had really created this::

    class MyLocalizedTests(LocalizedTestCase):
        def test_homepage_en(self):
            … # test English
        def test_homepage_es(self):
            … # test Spanish
