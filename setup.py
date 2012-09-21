#!/usr/bin/env python
from distutils.core import setup
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='django-longform',
    version='0.1.0',
    description='A Django application for longform blogging.',
    author='Martey Dodoo',
    author_email='django-longform@marteydodoo.com',
    url='https://github.com/martey/django-longform',
    license='MIT',
    py_modules=[
        'longform',
    ],
    long_description=read("README.rst"),
    classifiers=[],
)
