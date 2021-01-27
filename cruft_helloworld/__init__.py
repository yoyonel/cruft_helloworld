import os
import sys

from pkg_resources import get_distribution

__version__ = get_distribution("cruft_helloworld").version

if sys.platform == "win32":
    os.environ["APPDATA"] = os.environ.get("APPDATA", "")
