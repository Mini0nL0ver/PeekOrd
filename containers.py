from typing import *

T = TypeVar("T")


class PeekProxy(Generic[T]):
    def __init__(self, own: 'PeekOrdCol[T]', val: T):
        self.inner: T = val
        self._owner: 'PeekOrdCol'[T] = own

    def __repr__(self) -> str:
        return "PeekProxy(" + str(self.inner) + ")"

    def __lt__(self, other: 'PeekProxy[T]') -> bool:
        result = self.inner < other.inner
        entry = None
        if result:
            entry = PeekOrdLogEntry(self, other)
        else:
            entry = PeekOrdLogEntry(other, self)
        self._owner.get_or_make_log(other._owner).entries.append(entry)
        return result

    def __gt__(self, other: 'PeekProxy[T]') -> bool:
        result = self.inner > other.inner
        entry = None
        if result:
            entry = PeekOrdLogEntry(other, self)
        else:
            entry = PeekOrdLogEntry(self, other)
        self._owner.get_or_make_log(other._owner).entries.append(entry)
        return result


class PeekOrdCol(Generic[T]):
    def __init__(self, *args: T):
        self._objs: Set[PeekProxy[T]] = set({PeekProxy(self, val) for val in args})
        self._logs: Dict[PeekOrdCol[T], PeekOrdLog[T]] = dict()

    def __repr__(self) -> str:
        return "PeekOrdCol" + str(self._objs)

    def as_tup(self) -> Tuple[PeekProxy[T]]:
        return tuple(self._objs)

    def get_or_make_log(self, other: 'PeekOrdCol[T]') -> 'PeekOrdLog[T]':
        if other not in self._logs.keys():
            log = PeekOrdLog(self, other)
            self._logs[other] = log
            other._logs[self] = log
        # self._logs[other] is defined
        return self._logs[other]


class PeekOrdLog(Generic[T]):
    def __init__(self, list_a: PeekOrdCol[T], list_b: PeekOrdCol[T]):
        self._lists: Tuple[PeekOrdCol[T], PeekOrdCol[T]] = (list_a, list_b)
        self.entries: List[PeekOrdLogEntry[T]] = list()

    def __repr__(self) -> str:
        return "PeekOrdLog" + str(self.entries)


class PeekOrdLogEntry(Generic[T]):
    def __init__(self, a: PeekProxy[T], b: PeekProxy[T]):
        self.lft_lt_rgh: Tuple[PeekProxy[T], PeekProxy[T]] = (a, b)

    def __repr__(self) -> str:
        return "PeekOrdLogEntry(" + str(self.lft_lt_rgh[0]) + " < " + str(self.lft_lt_rgh[1]) + ")"
