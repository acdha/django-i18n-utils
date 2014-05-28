#!/usr/bin/env python

from setuptools import setup

setup(name="django-i18n-utils",
      version="1.1.0",

      packages=["django_i18n_utils"],

      author="Chris Adams",
      author_email="chris@improbable.org",

      description="Utilities for localized Django projects",
      long_description=open('README.rst').read(),
      license="MIT License",
      keywords="django i18n",
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Web Environment',
          'Framework :: Django',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Software Development :: Localization',
      ],
      url="https://pypi.python.org/pypi/django-i18n-utils")
