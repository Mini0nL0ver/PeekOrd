from typing import TypeVar, Generic, List, Tuple  # ..., Callable

T = TypeVar("T")


class PeekProxy(Generic[T]):
    def __init__(self, own: 'PeekOrdList'[T], val: T):
        self.inner = val
        self.owner = own


class PeekOrdList(Generic[T], List[PeekProxy[T]]):
    def __init__(self, *args: List[T]):
        list.__init__(self, [PeekProxy(self, val) for val in args])
        self.logs: List['PeekOrdLog'[T]] = list()


class PeekOrdLog(Generic[T]):
    def __init__(self, list_a: PeekOrdList[T], list_b: PeekOrdList[T]):
        self.lists: Tuple[PeekOrdList[T], PeekOrdList[T]] = (list_a, list_b)
        self.ord_log: List[PeekOrdLogEntry[T]] = list()


class PeekOrdLogEntry(Generic[T]):
    def __init__(self, a: PeekProxy[T], b: PeekProxy[T]):
        self.lft_lt_rgh: Tuple[PeekProxy[T], PeekProxy[T]] = (a, b)
