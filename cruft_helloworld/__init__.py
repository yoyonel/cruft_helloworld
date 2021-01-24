import os
import sys

"""
To prevent this error when imported pyfiglet under Windows platform:
  __________________ ERROR collecting cruft_helloworld/app.py ___________________
  cruft_helloworld\app.py:26: in <module>
      import pyfiglet
  .tox\py38\lib\site-packages\pyfiglet\__init__.py:59: in <module>
      SHARED_DIRECTORY = os.path.join(os.environ["APPDATA"], "pyfiglet")
  c:\hostedtoolcache\windows\python\3.8.6\x64\lib\os.py:675: in __getitem__
      raise KeyError(key) from None
  E   KeyError: 'APPDATA'
"""  # noqa: W605
if sys.platform == 'win32':
    os.environ["APPDATA"] = os.environ.get("APPDATA", "")
