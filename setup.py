#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'requests']

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Fernando Aguilar",
    author_email='aguilarf47@gmail.com',
    python_requires='!=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Send slack messages directly from codebuild to slack.",
    entry_points={
        'console_scripts': [
            'codebuildtoslack=codebuildtoslack.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='codebuildtoslack',
    name='codebuildtoslack',
    packages=find_packages(include=['codebuildtoslack', 'codebuildtoslack.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/fernandoaguilar/codebuildtoslack',
    version='0.1.0',
    zip_safe=False,
)
