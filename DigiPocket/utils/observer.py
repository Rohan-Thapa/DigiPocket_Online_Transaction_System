from typing import Callable, List

class Observer:
    def __init__(self):
        self._subscribers: List[Callable] = []

    def register(self, fn: Callable):
        self._subscribers.append(fn)

    def notify(self, *args, **kwargs):
        for fn in self._subscribers:
            fn(*args, **kwargs)