import pathlib
import re

from setuptools import setup, find_packages

_HERE = pathlib.Path(__file__).parent


def _resolve_path(*parts):
    """Get a filename from a list of path components, relative to this file."""
    return _HERE.joinpath(*parts).absolute()


def _read(*parts):
    """Read a file's contents into a string."""
    filename = _resolve_path(*parts)
    return filename.read_text()


__INIT__ = _read('src', 'py_info', '__init__.py')


def _get_package_variable(name):
    pattern = rf'^{name} = [\'"](?P<value>[^\'"]*)[\'"]'
    match = re.search(pattern, __INIT__, flags=re.M)
    if match:
        return match.group('value')
    raise RuntimeError(f'Cannot find variable {name}')


setup(
    name=_get_package_variable('__package__'),
    version=_get_package_variable('__version__'),
    description=_get_package_variable('__description__'),
    url=_get_package_variable('__url__'),
    author=_get_package_variable('__author__'),
    author_email=_get_package_variable('__author_email__'),
    long_description=_read('README.md'),
    long_description_content_type='text/markdown',
    packages=find_packages('src', exclude=['*.tests']),
    package_dir={
        '': 'src',
    },
    entry_points={
        'console_scripts': [
            'py_info = py_info:py_info',
        ],
    },
    extras_require={
        'dev': [
            'pytest',
            'coverage',
        ],
    },
    zip_safe=False,
)
