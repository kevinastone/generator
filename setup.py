#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'six',
]

test_requirements = [
    'nose',
    'mock',
]


if sys.version_info < (2, 7):
    # py26 needs unittest2 backport
    test_requirements.append('unittest2')


setup(
    name='test-generator',
    version='0.1.2',
    description="Generator is a helper for generating test methods for nose while still using unittest",
    long_description=readme + '\n\n' + history,
    author="Kevin Stone",
    author_email='kevinastone@gmail.com',
    url='https://github.com/kevinastone/generator',
    packages=[
        'generator',
    ],
    package_dir={'generator':
                 'generator'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='generator',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    setup_requires=['nose>=1.0'],
    test_suite='tests',
    tests_require=test_requirements
)
