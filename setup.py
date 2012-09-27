#!/usr/bin/env python
from setuptools import setup


setup(
    name='django-longform',
    version='0.1.3',
    description='A Django application for longform blogging.',
    author='Martey Dodoo',
    author_email='django-longform@marteydodoo.com',
    url='https://github.com/martey/django-longform',
    license='MIT',
    packages=['longform'],
    long_description=open('README.rst').read(),
    classifiers=[],
    install_requires=[
        'django',
        'django-markdown',
        'django-taggit',
        'markdown',
    ],
)
