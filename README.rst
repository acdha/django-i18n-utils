=================================
Django Internationalization Utils
=================================


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
