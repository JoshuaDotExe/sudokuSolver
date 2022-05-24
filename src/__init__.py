import logging
from os import getcwd

CWD = getcwd()
__version__ = "0.1.2"


LOGSOLVE_FORMAT = '%(name)-12s %(levelname)-8s %(message)s'
LOGSOLVE = logging.getLogger('SOLVED')


LOGDEBUG_FORMAT = '%(name)-12s %(levelname)-8s %(message)s'
LOGDEBUG = logging.getLogger('DEBUG')
