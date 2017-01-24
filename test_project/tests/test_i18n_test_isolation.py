# encoding: utf-8
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import unittest

from django.test import TestCase
from django.utils import translation
from django.utils.translation import ugettext as _

from django_i18n_utils.testcases import LocalizedTestCase
from django_i18n_utils.testclients import TranslationSafeTestClient


class TestActiveLanguageLeak(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestActiveLanguageLeak, cls).setUpClass()
        # Avoid cross test-case contamination:
        translation.deactivate_all()

    # The stock Django TestCase doesn't reset the translation state between tests
    def test_part_1(self):
        translation.activate('es')
        self.assertEqual('Enero', _('January'))

    @unittest.expectedFailure
    def test_part_2(self):
        # Will fail if test_part_1 ran first because the es locale is still active:
        self.assertEqual('January', _('January'))

    def test_part_3(self):
        translation.deactivate_all()
        self.assertEqual('January', _('January'))


class TestLocaleMiddlewareLeak(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestLocaleMiddlewareLeak, cls).setUpClass()

        # Avoid cross test-case contamination:
        translation.deactivate_all()

    # The stock Django TestCase doesn't reset the translation state between tests
    def test_part_1(self):
        resp = self.client.get('/es/month-name/', follow=True)
        self.assertEqual(resp.content.decode('utf-8'), 'Enero')

        # Confirm the leak:
        self.assertEqual('Enero', _('January'))

    @unittest.expectedFailure
    def test_part_2(self):
        # Will fail if test_part_1 ran first because the es locale is still active:
        self.assertEqual('January', _('January'))

    def test_part_3(self):
        # Confirm the leak hasn't been fixed:
        self.assertEqual('Enero', _('January'))

        resp = self.client.get('/en/month-name/', follow=True)
        # Merely accessing an Enlish page will reset the locale:
        self.assertEqual('January', _('January'))


class TestTranslationSafeTestClient(TestCase):
    client_class = TranslationSafeTestClient

    @classmethod
    def setUpClass(cls):
        super(TestTranslationSafeTestClient, cls).setUpClass()

        # Avoid cross test-case contamination:
        translation.deactivate_all()

    def test_part_1(self):
        resp = self.client.get('/es/month-name/', follow=True)
        self.assertEqual(resp.content.decode('utf-8'), 'Enero')

    def test_part_2(self):
        self.assertEqual('January', _('January'))

        resp = self.client.get('/en/month-name/', follow=True)
        self.assertEqual(resp.content.decode('utf-8'), 'January')

        self.assertEqual('January', _('January'))

    def test_part_3(self):
        self.assertEqual('January', _('January'))

        resp = self.client.get('/es/month-name/', follow=True)
        self.assertEqual(resp.content.decode('utf-8'), 'Enero')

        self.assertEqual('January', _('January'))

    def test_part_4(self):
        translation.deactivate_all()
        self.assertEqual('January', _('January'))


class TestLocalizedTestCase(LocalizedTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestLocalizedTestCase, cls).setUpClass()

        # Avoid cross test-case contamination:
        translation.deactivate_all()

    def test_localized(self):
        if translation.get_language() == 'es':
            self.assertEqual('Enero', _('January'))
        elif translation.get_language() == 'en':
            self.assertEqual('January', _('January'))

    def test_localized(self):
        resp = self.client.get('/month-name/', follow=True)
        self.assertEqual(resp.content.decode('utf-8'), _('January'))
