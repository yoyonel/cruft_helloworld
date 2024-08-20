import os
import sys

# https://docs.python.org/3.11/library/importlib.metadata.html#distributions
from importlib.metadata import distribution

__project_name__ = "cruft_helloworld"
__version__ = distribution(__project_name__).version

if sys.platform == "win32":
    os.environ["APPDATA"] = os.environ.get("APPDATA", "")
