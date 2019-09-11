"""
"""

import re
from setuptools import setup, find_packages


with open('watch_diff/__init__.py') as f:
    version = re.search(r'__version__ = \'(\d+\.\d+\.\d+)\'', f.read()).group(1)

with open('README.md') as f:
    long_description = f.read()

setup(
    name='watch-diff',
    version=version,
    description='Watch command output and get notified on changes',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Francis Bergin',
    author_email='me@francisbergin.com',
    python_requires='>=3.4',
    url='https://github.com/francisbergin/watch-diff',
    packages=['watch_diff'],
    extras_require={
        'dev': [
            'setuptools==41.2.0',
            'tox==3.14.0',
            'twine==1.14.0',
            'wheel==0.33.6',
        ]
    },
    license='MIT',
    entry_points={
        'console_scripts': [
            'watch-diff = watch_diff.__main__:main',
        ],
    },
)
