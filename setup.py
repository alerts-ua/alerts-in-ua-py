from setuptools import setup, find_packages

setup(
    name='alerts-in-ua',
    version='0.1.0',
    author='Ukrzen Team',
    author_email='api@alerts.in.ua',
    url='https://github.com/alerts-ua/alerts-in-ua-py',
    description='Python library for alerts.in.ua API',
    packages=find_packages(),
    install_requires=[
        'aiohttp', 'requests'
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)