from functools import partial
from syn.base_utils import compose
from syn.python.b import Statement, from_source, from_ast, Pass, Num, Name, \
    Assign, Return

mparse = compose(partial(from_source, mode='exec'), str)

#-------------------------------------------------------------------------------
# Utilities

def examine(s, s2=None):
    if s2 is None:
        s2 = s
    tree = mparse(s)
    assert tree.emit() == s2
    tree2 = from_ast(tree.to_ast(), mode='exec')
    assert tree2.emit() == s2

#-------------------------------------------------------------------------------
# Statement

def test_statement():
    Statement

#-------------------------------------------------------------------------------
# Assign

def test_assign():
    examine('a = 1')
    examine('a = b = 1')
    examine('a, b = 1', '(a, b) = 1')

    a = Assign([Name('x')], Num(1))
    assert a.emit() == 'x = 1'
    assert a.emit(indent_level=1) == '    x = 1'
    assert a.transform().emit() == 'x = 1'

    a = Assign([Name('x'), Name('y')], Num(1))
    assert a.emit() == 'x = y = 1'
    assert a.emit(indent_level=1) == '    x = y = 1'
    assert a.transform().emit() == 'x = y = 1'

#-------------------------------------------------------------------------------
# Return

def test_return():
    examine('return')
    examine('return 1')

    r = Return()
    assert r.emit() == 'return'
    assert r.emit(indent_level=1) == '    return'
    assert r.transform().emit() == 'return'

    r = Return(Num(1))
    assert r.emit() == 'return 1'
    assert r.emit(indent_level=1) == '    return 1'
    assert r.transform().emit() == 'return 1'

#-------------------------------------------------------------------------------
# Import

def test_import():
    examine('import foo')
    examine('import foo, bar, baz')
    examine('import foo, bar as baz')
    examine('import foo as bar, baz')

#-------------------------------------------------------------------------------
# Empty Statements

def test_empty_statements():
    examine('break')
    examine('continue')
    examine('pass')

    p = Pass()
    assert p.emit() == 'pass'
    rp = p.add_return()
    assert rp.emit() == 'return'

#-------------------------------------------------------------------------------

if __name__ == '__main__': # pragma: no cover
    from syn.base_utils import run_all_tests
    run_all_tests(globals(), verbose=True, print_errors=False)
