from setuptools import setup, find_packages
import os
import re


NAME = 'secure-user-data'
KEYWORDS = 'secure user data link-society microservice'
DESC = 'Securely store and access user identifiable data'
URL = 'https://git.link-society.com/link-society/secure-user-data'
AUTHOR = 'Link Society'
AUTHOR_EMAIL = 'contact@link-society.com'
LICENSE = 'Apache Public License'
REQUIREMENTS = [
    'attrs>=18.1.0',
    'sanic>=0.7.0',
    'wtforms>=2.1',
    'aiohttp>=3.2.1',
    'aiodns>=1.1.1',
    'python-decouple>=3.1',
    'logbook>=1.3.3',
    'click>=6.7',
    'cryptography>=2.2.2',
    'motor>=1.2.1'
]

ENTRY_POINTS = {
    'console_scripts': [
        'sud-service=sud.cli.service:main'
    ]
}

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: Implementation :: CPython'
]


def get_cwd():
    return os.path.dirname(os.path.abspath(os.path.expanduser(__file__)))


def get_version(default='0.1'):
    path = os.path.join(get_cwd(), 'sud', '__init__.py')

    with open(path) as f:
        stream = f.read()
        regex = re.compile(r'.*__version__ = \'(.*?)\'', re.S)
        version = regex.match(stream)

        if version is None:
            version = default

        else:
            version = version.group(1)

    return version


def get_long_description():
    path = os.path.join(get_cwd(), 'README.rst')
    desc = None

    if os.path.exists(path):
        with open(path) as f:
            desc = f.read()

    return desc


def get_test_suite():
    return 'tests'


setup(
    name=NAME,
    keywords=KEYWORDS,
    version=get_version(),
    url=URL,
    description=DESC,
    long_description=get_long_description(),
    license=LICENSE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages=find_packages(),
    test_suite=get_test_suite(),
    install_requires=REQUIREMENTS,
    entry_points=ENTRY_POINTS,
    classifiers=CLASSIFIERS
)
