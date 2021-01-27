__version__ = "0.3.0"

import os
import sys

if sys.platform == "win32":
    os.environ["APPDATA"] = os.environ.get("APPDATA", "")
