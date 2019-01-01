# coding: utf-8

"""Set up the packages for distribution and installation."""

from setuptools import setup
from basic_lang import version

setup(
    name='basic_lang',
    version=version.VERSION,
    author='Ken Guyton',
    author_email='kenguyton@gmail.com',
    packages=['basic_lang'],
    include_package_data=True,
    scripts=['bin/basic_run.py']
)
