from typing import TypeVar, Generic, List  # ..., Callable

T = TypeVar("T")


class PeekProxy(Generic[T]):
    def __init__(self, val: T):
        self.inner = val


class PeekOrdList(Generic[T], List[PeekProxy[T]], list):
    pass
