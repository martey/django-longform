#!/usr/bin/env python
from distutils.core import setup


setup(
    name='django-longform',
    version='0.1.1',
    description='A Django application for longform blogging.',
    author='Martey Dodoo',
    author_email='django-longform@marteydodoo.com',
    url='https://github.com/martey/django-longform',
    license='MIT',
    py_modules=[
        'longform',
    ],
    long_description=open('README').read(),
    classifiers=[],
)
