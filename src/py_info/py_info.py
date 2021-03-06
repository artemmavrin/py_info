"""Display information about the current system, Python, and Python packages."""

_DEFAULT_PACKAGES = [
    'matplotlib',
    'numpy',
    'pandas',
    'scipy',
    'sklearn',
    'tensorflow',
]


def py_info(*packages: str, file=None):
    import argparse
    import collections
    import importlib
    import os
    import platform
    import sys
    import warnings

    if not packages:
        # No packages specified, parse command line arguments to get packages,
        # falling back to default packages if no command line arguments are
        # given
        parser = argparse.ArgumentParser(
            description='Get information about Python and the system.',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
        parser.add_argument('package', nargs='*', default=_DEFAULT_PACKAGES,
                            help='One or more Python packages.')
        args = parser.parse_args()
        packages = args.package
    elif len(packages) == 1 and not isinstance(packages[0], str):
        # Allow the function to be passed a list of packages as the first
        # positional argument (i.e., py_info(['numpy', 'scipy']) in addition to
        # py_info('numpy', 'scipy')
        packages = packages[0]

    packages = list(map(str, packages))

    # String to use for missing data
    unknown = '???'

    # System search path
    path = os.environ.get('PATH', unknown)

    # Convert path to a multi-line string, one line per component
    path = '\n'.join(map(str.strip, path.split(os.pathsep)))

    # Non-Python information about the current system
    system_info = [
        ('Platform', platform.platform() or unknown),
        ('Hostname', platform.node() or unknown),
        ('Machine Type', platform.machine() or unknown),
        ('Processor', platform.processor() or unknown),
        ('Byte Order', sys.byteorder + '-endian'),
        ('Working Directory', os.getcwd()),
        ('Path', path),
    ]

    # Python information
    python_info = [
        ('Version', sys.version),
        ('Executable', sys.executable),
        ('Implementation', platform.python_implementation()),
        ('Python Path', '\n'.join(filter(None, sys.path[1:])).strip()),
    ]

    def get_module(package: str):
        """Try to load a module."""
        try:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                return importlib.import_module(package)
        except ImportError:
            return None

    def version(package: str):
        """Try to get the version string of a package."""
        module = get_module(package)
        if module is None:
            return None

        v = getattr(module, '__version__', unknown)

        return v

    package_info = [(package, version(package)) for package in packages]

    # Python dicts are ordered in Python 3.7:
    # https://mail.python.org/pipermail/python-dev/2017-December/151283.html
    # https://docs.python.org/3.7/library/stdtypes.html#typesmapping
    # But in previous versions, insertion order is not guaranteed to be
    # maintained (although it is in the CPython implementation of Python 3.6).
    system_info = collections.OrderedDict(system_info)
    python_info = collections.OrderedDict(python_info)
    package_info = collections.OrderedDict(package_info)

    # Setup for pretty-printing
    all_keys = set().union(system_info, python_info, package_info)
    padding = max(map(len, all_keys))
    separator = ': '

    def pprint_info(label, mapping):
        """Pretty-print an information mapping, including alignment and
        indentation stuff.
        """
        print('', label, '=' * len(label), sep='\n', file=file)
        for k, v in mapping.items():
            if not isinstance(v, str):
                v = str(v)
            if '\n' in v:
                # Make each new line start at the appropriate indentation level
                v = v.replace('\n', '\n' + (' ' * (padding + len(separator))))
            print(k.rjust(padding), separator, v, sep='', file=file)

    pprint_info('System', system_info)
    pprint_info('Python', python_info)
    pprint_info('Packages', package_info)
