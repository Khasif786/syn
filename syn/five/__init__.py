'''Additional Python 2/3 compatibility facilities.
'''
from .string import *
from .num import *
from six import PY2, PY3

# range-related
from six.moves import xrange
range = lambda *args, **kwargs: list(xrange(*args, **kwargs))

if PY2:
    raw_input = raw_input
else:
    raw_input = input

# For convenience, not compatibility
SET = (set, frozenset)

# from syn.base_utils import harvest_metadata, delete
# with delete(harvest_metadata, delete):
#     harvest_metadata('../metadata.yml')
