from multiprocessing import Manager
from queue import Queue, Empty
import pytest
from tx.functional.maybe import Just
from tx.parallex.dependentqueue import DependentQueue, Node


def test_dep():
    with Manager() as manager:
        dq = DependentQueue(manager, None)

        id3 = dq.put(3)
        id2 = dq.put(2, depends_on={id3})
        id1 = dq.put(1, depends_on={id3, id2})
        
        n, r, sr, f1 = dq.get(block=False)
        assert n == 3
        assert r == {}
        dq.complete(f1, {}, Just(6))
        n, r, sr, f2 = dq.get(block=False)
        assert n == 2
        assert r == {f1: 6}
        dq.complete(f2, {}, Just(5))
        n, r, sr, f = dq.get(block=False)
        assert n == 1
        assert r == {f2: 5, f1: 6}
        dq.complete(f, {}, Just(4))
        n, r, sr, f = dq.get(block=False)
        assert n is None
        with pytest.raises(Empty):
            dq.get(block=False)
    
