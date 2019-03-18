#!/usr/bin/python

from distutils.core import setup
from distutils.command.install_data import install_data

import glob
import os
import re

setup(
    name             = 'treasury',
    version          = '0.1',
    url              = 'none',
    author           = 'Bryce Harrington',
    author_email     = 'bryce@bryceharrington.org',
    description      = 'Extracts and presents financial data from Ledger',
    platforms        = ['any'],
    requires         = ['argparse', 'ruamel', 'pprint'],
    packages         = [
        'treasury'
        ],
    package_data = { },
    data_files = [ ],
    scripts = glob.glob('scripts/*'),
)
