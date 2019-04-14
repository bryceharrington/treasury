#!/usr/bin/python3

from setuptools import setup

import glob

setup(
    name             = 'treasury',
    version          = '0.1',
    url              = 'none',
    author           = 'Bryce Harrington',
    author_email     = 'bryce@bryceharrington.org',
    description      = 'Extracts and presents financial data from Ledger',
    long_description = open('README.md', 'rt').read()
    platforms        = ['any'],
    requires         = ['argparse',
                        'ruamel',
                        'pprint',

                        'flask',
                        'flask_restful'
    ],
    setup_requires   = ['pytest-runner'],
    packages         = [
        'treasury'
        ],
    package_data = { },
    data_files = [ ],
    scripts = glob.glob('scripts/*'),

    tests_require = ['pytest'],
)
