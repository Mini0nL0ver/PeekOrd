from typing import *
from time import sleep, time

T = TypeVar("T")


class PeekOrdProxy(Generic[T]):
    def __init__(self, owner: 'PeekOrdCol[T]', val: T):
        self.val: T = val
        self._owner: 'PeekOrdCol'[T] = owner

    def __repr__(self) -> str:
        return "PeekOrdProxy(" + str(self.val) + ")"

    def __lt__(self, other: 'PeekOrdProxy[T]') -> bool:
        result = self.val < other.val
        _entry = None
        if result:
            _entry = PeekOrdEntry(self, other)
        else:
            _entry = PeekOrdEntry(other, self)
        self._owner.get_or_make_log(other._owner).entries.append(_entry)
        return result

    def __gt__(self, other: 'PeekOrdProxy[T]') -> bool:
        result = self.val > other.val
        _entry = None
        if result:
            _entry = PeekOrdEntry(other, self)
        else:
            _entry = PeekOrdEntry(self, other)
        self._owner.get_or_make_log(other._owner).entries.append(_entry)
        return result


class PeekOrdCol(Generic[T]):
    def __init__(self, *args: T):
        self._objs: Set[PeekOrdProxy[T]] = set({PeekOrdProxy(self, val) for val in args})
        self._logs: Dict[PeekOrdCol[T], PeekOrdLog[T]] = dict()

    def __repr__(self) -> str:
        return "PeekOrdCol" + str(self._objs)

    def as_tup(self) -> Tuple[PeekOrdProxy[T]]:
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
        self.entries: List[PeekOrdEntry[T]] = list()

    def __repr__(self) -> str:
        return "PeekOrdLog" + str(self.entries)


class PeekOrdEntry(Generic[T]):
    def __init__(self, a: PeekOrdProxy[T], b: PeekOrdProxy[T]):
        self.lft_lt_rgh: Tuple[PeekOrdProxy[T], PeekOrdProxy[T]] = (a, b)
        self.timestamp: float = time()
        sleep(0.001)

    def __repr__(self) -> str:
        return "PeekOrdEntry(" + str(self.lft_lt_rgh[0]) + " < " + str(self.lft_lt_rgh[1]) + ")"

    def __lt__(self, other: 'PeekOrdEntry[T]') -> bool:
        return self.timestamp < other.timestamp

    def __gt__(self, other: 'PeekOrdEntry[T]') -> bool:
        return self.timestamp > other.timestamp

    def __le__(self, other: 'PeekOrdEntry[T]') -> bool:
        return (self == other) | (self < other)

    def __ge__(self, other: 'PeekOrdEntry[T]') -> bool:
        return (self == other) | (self > other)


class PeekOrdTimeline(Generic[T]):
    def __init__(self, *logs: PeekOrdLog[T]):
        entries: List[PeekOrdEntry[T]] = list()
        for log in logs:
            entries.extend(log.entries)
        entries.sort()
        self._entries: Tuple[PeekOrdEntry[T], ...] = tuple(entries)

    def __getitem__(self, i: SupportsIndex) -> 'PeekOrdFrame[T]':
        return PeekOrdFrame(self, i.__index__())

    def past(self, i: SupportsIndex) -> Tuple[PeekOrdEntry[T], ...]:
        return self._entries[0: i.__index__()]


class PeekOrdFrame(Generic[T]):
    def __init__(self, timeline: PeekOrdTimeline[T], index: int):
        self.timeline: PeekOrdTimeline[T] = timeline
        self.index: int = index

    def __index__(self) -> int:
        return self.index

    def check_lt(self, a: PeekOrdProxy[T], b: PeekOrdProxy[T]) -> bool:
        gt_dict: Dict[PeekOrdProxy[T], Set[PeekOrdProxy[T]]] = dict()
        for entry in self.timeline.past(self):
            lhs: PeekOrdProxy[T] = entry.lft_lt_rgh[0]
            rhs: PeekOrdProxy[T] = entry.lft_lt_rgh[1]
            if lhs not in gt_dict.keys():
                gt_dict[lhs] = set()
            gt_dict[lhs].add(rhs)

        def lt(x: PeekOrdProxy[T], y: PeekOrdProxy[T], cache: Set[PeekOrdProxy[T]] = None) -> bool:
            if cache is None:
                cache = set()
            for gt in gt_dict[x]:
                if gt in cache:
                    return False
                elif gt is y:
                    return True
                elif lt(gt, y, cache):
                    return True
            cache.add(x)
            return False

        return lt(a, b)
