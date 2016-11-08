from six import PY2, PY3
from syn.five import xrange
from nose.tools import assert_raises
from syn.types.a import Type, String, Unicode, Bytes, \
    hashable, serialize, deserialize, estr, rstr, generate, visit, find_ne
from syn.types.a import enumerate as enumerate_
from syn.base_utils import is_hashable, assert_equivalent, subclasses, \
    on_error, elog, ngzwarn, is_unique

from syn.globals import TEST_SAMPLES as SAMPLES
SAMPLES //= 10
SAMPLES = max(SAMPLES, 1)
ngzwarn(SAMPLES, 'SAMPLES')

#-------------------------------------------------------------------------------
# string_enumval

def test_string_enumval():
    from syn.types.a.string import string_enumval, _STRING_ENUMVALS

    assert string_enumval(0) == ' '
    assert string_enumval(94) == '~'
    assert string_enumval(95) == '  '
    assert string_enumval(96) == ' !'
    #import ipdb; ipdb.set_trace()
    assert string_enumval(189) == ' ~'
    assert string_enumval(190) == '! '
    assert string_enumval(191) == '!!'

    assert _STRING_ENUMVALS[0] == ' '
    assert _STRING_ENUMVALS[191] == '!!'

#-------------------------------------------------------------------------------

def examine_string(cls, val):
    assert type(val) is cls.type
    assert is_hashable(hashable(val))
    assert deserialize(serialize(val)) == val
    assert isinstance(rstr(val), str)

    assert list(visit(val)) == list(val)
    assert find_ne(val, val) is None

    eitem = eval(estr(val))
    assert eitem == val
    assert type(eitem) is cls.type

#-------------------------------------------------------------------------------
# String

def test_string():
    s = u'abc'

    t = Type.dispatch(s)
    assert isinstance(t, String)

    if PY2:
        assert type(t) is Unicode
    else:
        assert type(t) is String

    assert hashable(s) == t.hashable() == s
    assert is_hashable(s)
    assert is_hashable(hashable(s))

    for cls in subclasses(String, [String]):
        if cls.type is None:
            continue

        for k in xrange(SAMPLES):
            val = cls.generate()
            with on_error(elog, examine_string, (cls, val)):
                examine_string(cls, val)

        buf = []
        last = None
        for item in enumerate_(cls.type, max_enum=10):
            assert type(item) is cls.type
            assert item != last
            buf.append(item)
            last = item

        assert is_unique(buf)

    # estr edge cases

    cases = ["abc'de\r7fghi", "\x00"]
    for case in cases:
        assert eval(estr(case)) == case

#-------------------------------------------------------------------------------
# Unicode

def test_unicode():
    if PY2:
        gen = generate(unicode)
        assert isinstance(gen, unicode)

#-------------------------------------------------------------------------------
# Bytes

def test_bytes():
    if PY3:
        gen = generate(bytes)
        assert isinstance(gen, bytes)

#-------------------------------------------------------------------------------

if __name__ == '__main__': # pragma: no cover
    from syn.base_utils import run_all_tests
    run_all_tests(globals(), verbose=True, print_errors=False)
