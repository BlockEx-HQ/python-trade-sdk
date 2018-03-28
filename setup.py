from setuptools import setup, find_packages

setup(
    name='blockex-tradeapi',
    version='1.0.0rc1',
    description='Python client library for BlockEx Trade API',
    url='https://github.com/blockex/tradeapi',
    author='Dobromir Petrov, BlockEx',
    author_email='dobromir.petrov@blockex.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    keywords='api client blockex trade api',
    install_requires=['enum34', 'six', 'requests'],
    extras_require={
        'test': ['mock'],
    },
    project_urls={
        'Bug Reports': 'https://github.com/blockex/tradeapi/issues',
        'Source': 'https://github.com/blockex/tradeapi',
    },
)
