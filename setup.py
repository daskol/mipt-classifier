#!/usr/bin/env python3
#   encoding: utf8
#   setup.py

"""MIPT Student Classifier
"""

from setuptools import setup, find_packages


DOCLINES = (__doc__ or '').split('\n')

CLASSIFIERS = """\
Development Status :: 4 - Beta
Environment :: Console
Intended Audience :: Developers
Intended Audience :: End Users/Desktop
Intended Audience :: Information Technology
Intended Audience :: Other Audience
License :: OSI Approved :: MIT License
Natural Language :: Russian
Operating System :: POSIX :: Linux
Programming Language :: Python
Programming Language :: Python :: 3.5
Topic :: Internet
Topic :: Office/Business
Topic :: Utilities
"""

PLATFORMS = [
    'Linux',
]

MAJOR = 0
MINOR = 0
PATCH = 0

VERSION = '{0:d}.{1:d}.{2:d}'.format(MAJOR, MINOR, PATCH)


def setup_package():
    setup(name='miptclass',
         version=VERSION,
         description = DOCLINES[0],
         long_description = '\n'.join(DOCLINES[2:]),
         author='Daniel Bershatsky',
         author_email='daniel.bershatsky@skolkovotech.ru',
         license='MIT',
         platforms=PLATFORMS,
         classifiers=[line for line in CLASSIFIERS.split('\n') if line],
         packages=find_packages(),
         entry_points={
             'console_scripts': [
                 'mipt-classifier=miptclass.cli:main',
            ],
         },
    )      


if __name__ == '__main__':
    setup_package()
