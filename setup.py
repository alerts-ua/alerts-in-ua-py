from setuptools import setup, find_packages

import pathlib
import re

here = pathlib.Path(__file__).parent.resolve()  # current path
long_description = (here / 'README.md').read_text(encoding='utf-8')  # Get the long description from the README file

setup(
    name='alerts-in-ua',
    version='0.1.5',
    author='Ukrzen Team',
    author_email='api@alerts.in.ua',
    url='https://github.com/alerts-ua/alerts-in-ua-py',
    description='Python library for alerts.in.ua API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        'aiohttp', 'requests'
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)