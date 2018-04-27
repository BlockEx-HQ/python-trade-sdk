import os
import sys

from setuptools import setup

version = "0.0.3"

dependency_links = []
install_requires = ['enum34', 'requests']

if sys.version_info >= (3, 5, 3):
    install_requires.append('signalr-client-aio')

if sys.version_info >= (2, 7) and sys.version_info < (3, 0):
    install_requires.append('mock')

setup(
    name='blockex.trade-sdk',
    version=version,
    description='BlockEx trade API client SDK',
    url='https://blockexmarkets.com',
    author='BlockEx dev team',
    author_email='developers@blockex.com',
    license='MIT',
    keywords='api client blockex trade sdk',
    install_requires=install_requires,
    dependency_links=dependency_links,
    extras_require={
        'test': ['mock', 'pytest'],
    },
    packages=[d[0].replace("/", ".") for d in os.walk("blockex.tradeapi") if not d[0].endswith("__pycache__")],
    project_urls={
        'Bug Reports': 'https://bitbucket.org/blockex/python-sdk/issues',
        'Source': 'https://bitbucket.org/blockex/python-sdk',
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6"
    ]
)
