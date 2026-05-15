from cfgts._version import VERSION
from cfgts.cfgts import CFGTS

__version__ = VERSION

__all__ = ["CFGTS"]

import sys

assert sys.version_info >= (3, 11), "Python 3.10 and below is not supported by cfgts"
