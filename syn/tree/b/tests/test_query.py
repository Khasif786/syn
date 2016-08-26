from nose.tools import assert_raises
from syn.tree.b.query import Query

#-------------------------------------------------------------------------------
# Query

def test_query():
    q = Query()
    assert_raises(NotImplementedError, q)

#-------------------------------------------------------------------------------

if __name__ == '__main__': # pragma: no cover
    from syn.base_utils import run_all_tests
    run_all_tests(globals(), verbose=True, print_errors=False)