import re
import six
import types
import inspect

#-------------------------------------------------------------------------------

import six.moves.builtins # pylint: disable=E0401
builtins = list(vars(six.moves.builtins).values())

# NOTE: for classes only (not objects)
if six.PY2:
    METHOD_TYPES = (types.MethodType, types.BuiltinMethodType)
else:
    METHOD_TYPES = (types.MethodType, types.BuiltinMethodType,
                    types.FunctionType, types.BuiltinFunctionType)

#-------------------------------------------------------------------------------
# Class utilities

def mro(cls):
    if cls is type:
        return [type]
    elif isinstance(cls, type):
        try:
            return cls.mro()
        except TypeError:
            return [cls]
    else:
        return type(cls).mro()

def hasmethod(x, name):
    val = getattr(x, name, None)
    if isinstance(x, type):
        return isinstance(val, METHOD_TYPES)
    return inspect.ismethod(val)

#-------------------------------------------------------------------------------
# Module utilities

def import_module(modname):
    if '.' in modname:
        module = modname.split('.')[-1]
        mod = __import__(modname, fromlist=[module])
    else:
        mod = __import__(modname)
    return mod

#-------------------------------------------------------------------------------
# Exception utilities

def message(e):
    if hasattr(e, 'message'):
        return e.message
    if e.args:
        return e.args[0]
    return ''

#-------------------------------------------------------------------------------
# Unit Test Collection

NOSE_PATTERN = re.compile('(?:^|[\\b_\\.-])[Tt]est')

def _identify_testfunc(s):
    return bool(re.search(NOSE_PATTERN, s))

def run_all_tests(env, verbose=False, print_errors=False, exclude=None):
    import sys
    import traceback

    if exclude is None:
        exclude = []

    testfuncs = []
    for key in env:
        if key != 'run_all_tests':
            if key not in exclude:
                if _identify_testfunc(key):
                    if hasattr(env[key], '__call__'):
                        if isinstance(env[key], types.FunctionType):
                            testfuncs.append(key)

    for tf in testfuncs:
        if verbose:
            print(tf)
        if print_errors:
            try:
                env[tf]()
            except: # pylint: disable=W0702
                traceback.print_exception(*sys.exc_info())
        else:
            env[tf]()
        
#-------------------------------------------------------------------------------
# Testing utilities

def assert_equivalent(o1, o2):
    '''Asserts that o1 and o2 are distinct, yet equivalent objects
    '''
    if not (isinstance(o1, type) and isinstance(o2, type)):
        assert o1 is not o2
    assert o1 == o2
    assert o2 == o1

def assert_inequivalent(o1, o2):
    '''Asserts that o1 and o2 are distinct and inequivalent objects
    '''
    if not (isinstance(o1, type) and isinstance(o2, type)):
        assert o1 is not o2
    assert not o1 == o2 and o1 != o2
    assert not o2 == o1 and o2 != o1

def assert_deepcopy_idempotent(obj):
    '''Assert that obj does not change (w.r.t. ==) under repeated deepcopies
    '''
    from copy import deepcopy
    obj1 = deepcopy(obj)
    obj2 = deepcopy(obj1)
    obj3 = deepcopy(obj2)
    assert_equivalent(obj, obj1)
    assert_equivalent(obj, obj2)
    assert_equivalent(obj, obj3)
    assert type(obj) is type(obj3)

def assert_pickle_idempotent(obj):
    '''Assert that obj does not change (w.r.t. ==) under repeated picklings
    '''
    from six.moves.cPickle import dumps, loads
    obj1 = loads(dumps(obj))
    obj2 = loads(dumps(obj1))
    obj3 = loads(dumps(obj2))
    assert_equivalent(obj, obj1)
    assert_equivalent(obj, obj2)
    assert_equivalent(obj, obj3)
    assert type(obj) is type(obj3)

#-------------------------------------------------------------------------------
# __all__

__all__ = ('mro', 'hasmethod', 'import_module', 'message', 'run_all_tests',
           'assert_equivalent', 'assert_inequivalent',
           'assert_pickle_idempotent', 'assert_deepcopy_idempotent')

#-------------------------------------------------------------------------------