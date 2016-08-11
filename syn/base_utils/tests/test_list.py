from nose.tools import assert_raises

#-------------------------------------------------------------------------------
# ListView

def test_listview():
    from syn.base_utils import ListView

    lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    lv = ListView(lst, 2, 5)
    assert len(lv) == 3
    assert list(lv) == [2, 3, 4]

    assert lv[0] == 2
    assert lv[1] == 3
    assert lv[2] == 4
    assert lv[-1] == 4
    assert lv[-2] == 3
    assert lv[-3] == 2

    assert_raises(IndexError, lv.__getitem__, 3)
    assert_raises(IndexError, lv.__getitem__, -4)
    assert_raises(IndexError, lv.__setitem__, 3, 8)
    assert_raises(IndexError, lv.__delitem__, 3)

    lv[0] = 10
    assert lst == [0, 1, 10, 3, 4, 5, 6, 7, 8, 9]

    lv.pop(0)
    assert len(lv) == 2
    assert list(lv) == [3, 4]
    assert lst == [0, 1, 3, 4, 5, 6, 7, 8, 9]

    lv.append(10)
    assert list(lv) == [3, 4, 10]
    assert lst == [0, 1, 3, 4, 10, 5, 6, 7, 8, 9]

    lv.pop()
    assert list(lv) == [3, 4]
    assert lst == [0, 1, 3, 4, 5, 6, 7, 8, 9]

    lv.pop()
    lv.pop()
    assert list(lv) == []
    assert lst == [0, 1, 5, 6, 7, 8, 9]

    assert_raises(IndexError, lv.pop)

    lv = ListView(lst, 4, -1)
    assert len(lv) == 3
    assert list(lv) == [7, 8, 9]

    lv.insert(0, 10)
    assert list(lv) == [10, 7, 8, 9]
    assert lst == [0, 1, 5, 6, 10, 7, 8, 9]

    assert_raises(TypeError, ListView, 1, 0, 0)
    assert_raises(ValueError, ListView, [1, 2, 3], 2, 1)
    assert_raises(ValueError, ListView, [1, 2, 3], 5, 7)
    assert_raises(ValueError, ListView, [1, 2, 3], 0, 7)

#-------------------------------------------------------------------------------
# Query Utilities

def test_is_proper_sequence():
    from syn.base_utils import is_proper_sequence

    assert not is_proper_sequence(1)
    assert not is_proper_sequence('abc')
    assert is_proper_sequence(['a', 'b', 'c'])
    assert is_proper_sequence(('a', 'b', 'c'))

def test_is_flat():
    from syn.base_utils import is_flat

    assert is_flat([1, 2, 3])
    assert is_flat((1, 2, 3))
    assert is_flat('abc')
    assert is_flat(['a', 'b', 'c'])
    assert not is_flat([[], 2, 3])

    assert_raises(TypeError, is_flat, 1)

#-------------------------------------------------------------------------------
# Non-Modification Utilities

def test_indices_removed():
    from syn.base_utils import indices_removed
    
    lst = list(range(10))
    assert indices_removed(lst, (0, 5, 9)) == [1, 2, 3, 4, 6, 7, 8]
    assert indices_removed(tuple(lst), (0, 5, 9)) == (1, 2, 3, 4, 6, 7, 8)
    assert indices_removed(lst, lst) == []

    assert lst == list(range(10))

def test_flattened():
    from syn.base_utils import flattened

    assert flattened(5) == [5]
    assert flattened([1, 2]) == [1, 2]
    assert flattened((1, 2)) == [1, 2]
    assert flattened([1]) == [1]
    assert flattened([[1]]) == [1]

    assert flattened([[1, 2], [3, 4, 5]]) == [1, 2, 3, 4, 5]
    assert flattened([[1, (2, 3, [4]), [[5]]], [[3, (4, 5)]]]) == \
        [1, 2, 3, 4, 5, 3, 4, 5]

    assert flattened([1, [2, 3, [4, 5], 6], 7, [8, 9], 10]) == \
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    assert flattened([[]]) == []
    assert flattened([1, 2, [], 3, 4]) == [1, 2, 3, 4]
    assert flattened([1, 2, [[], 7, [[]]], 3, 4]) == [1, 2, 7, 3, 4]
    assert flattened([[], 1, 2]) == [1, 2]

#-------------------------------------------------------------------------------

if __name__ == '__main__': # pragma: no cover
    from syn.base_utils import run_all_tests
    run_all_tests(globals(), verbose=True, print_errors=False)
