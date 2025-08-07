from setuptools import setup, find_packages
import pathlib
import re

here = pathlib.Path(__file__).parent.resolve()  # current path
long_description = (here / 'README.md').read_text(encoding='utf-8')  # Get the long description from the README file

# Read version from __init__.py without importing
def get_version():
    init_file = here / 'alerts_in_ua' / '__init__.py'
    with open(init_file, 'r') as f:
        content = f.read()
        match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
        if match:
            return match.group(1)
        raise RuntimeError("Unable to find version string in __init__.py")

__version__ = get_version()

setup(
    name='alerts-in-ua',
    version=__version__,
    author='Ukrzen Team',
    author_email='api@alerts.in.ua',
    url='https://github.com/alerts-ua/alerts-in-ua-py',
    description='Python library for alerts.in.ua API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        'aiohttp', 'requests','pytz'
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)