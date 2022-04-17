from typing import *

T = TypeVar("T")


class PeekProxy(Generic[T]):
    def __init__(self, own: 'PeekOrdCol'[T], val: T):
        self.inner: T = val
        self._owner: 'PeekOrdCol'[T] = own

    def __lt__(self, other: 'PeekProxy'[T]) -> bool:
        result = self.inner < other.inner
        entry = None
        if result:
            entry = PeekOrdLogEntry(self, other)
        else:
            entry = PeekOrdLogEntry(other, self)
        # TODO: call owner to store log entry
        return result

    def __gt__(self, other: 'PeekProxy'[T]) -> bool:
        result = self.inner > other.inner
        entry = None
        if result:
            entry = PeekOrdLogEntry(other, self)
        else:
            entry = PeekOrdLogEntry(self, other)
        # TODO: call owner to store log entry
        return result


class PeekOrdCol(Generic[T]):
    def __init__(self, *args: List[T]):
        self._objs: Set[PeekProxy[T]] = set({PeekProxy(self, val) for val in args})
        self._logs: Dict[PeekOrdCol[T], PeekOrdLog[T]] = dict()


class PeekOrdLog(Generic[T]):
    def __init__(self, list_a: PeekOrdCol[T], list_b: PeekOrdCol[T]):
        self._lists: Tuple[PeekOrdCol[T], PeekOrdCol[T]] = (list_a, list_b)
        self.ord_log: List[PeekOrdLogEntry[T]] = list()


class PeekOrdLogEntry(Generic[T]):
    def __init__(self, a: PeekProxy[T], b: PeekProxy[T]):
        self.lft_lt_rgh: Tuple[PeekProxy[T], PeekProxy[T]] = (a, b)
