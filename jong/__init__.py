VERSION = (0, 0, 1)  # PEP 386
__version__ = ".".join([str(x) for x in VERSION])

from jong.db import Rss
from jong.core import main
from jong.load_data import load
