from pkg_resources import get_distribution

PACKAGE_NAME = "cruft_helloworld"
__version__ = get_distribution(PACKAGE_NAME).version
