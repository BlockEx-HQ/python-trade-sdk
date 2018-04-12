from setuptools import setup

version = "0.0.1"

setup(
    name='blockex.tradeapi',
    version=version,
    description='BlockEx trade API client SDK',
    url='https://blockexmarkets.com',
    author='BlockEx dev team',
    author_email='developers@blockex.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    license='MIT',
    keywords='api client blockex trade sdk',
    install_requires=['enum34', 'requests'],
    extras_require={
        'test': ['mock', 'pytest'],
    },
    packages=(
        "blockex.tradeapi",
    ),
    project_urls={
        'Bug Reports': 'https://bitbucket.org/blockex/python-sdk/issues',
        'Source': 'https://bitbucket.org/blockex/python-sdk',
    },
)
