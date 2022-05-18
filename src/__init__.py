import logging

__version__ = "0.1.2"


__SOLVED_FORMAT = '%(name)-12s %(levelname)-8s %(message)s'
SOLVED = logging.getLogger('SOLVED')

__DEBUG_FORMAT = '%(name)-12s %(levelname)-8s %(message)s'
DBUGR = logging.getLogger('DEBUG')
