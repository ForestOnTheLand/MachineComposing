import sys
import random


class RouletteSelection:

    def __init__(self, items: int) -> None:
        self._value_sum = 0
        self._index = 0
        self._total_items = items
        self._submitted_items = 0

    def submit(self, value: float) -> None:
        assert value >= 0
        self._value_sum += value
        if random.random() < value / (self._value_sum + sys.float_info.min):
            self._index = self._submitted_items
        self._submitted_items += 1

    def done(self) -> bool:
        return self._submitted_items >= self._total_items

    def selected_index(self) -> int:
        return self._index
