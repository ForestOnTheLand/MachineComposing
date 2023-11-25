from typing import List, Sequence, Optional, overload
from typing_extensions import Self
import random


class Note:
    """
    As is described in the paper, the `Note` is represented by `int`, ranging from
    `0`(included) to `28`(included). `0` stands for a break, `28` for a prolongation,
    and other numbers from `1` to `27` represents notes from F3(53) to G5(79) respectively.
    """
    # static member
    NAME_LIST = [
        " ", "F3", "#F3", "G3", "#G3", "A3", "#A3", "B3", "C4", "#C4", "D4", "#D4", "E4", "F4",
        "#F4", "G4", "#G4", "A4", "#A4", "B4", "C5", "#C5", "D5", "#D5", "E5", "F5", "#F5", "G5",
        "-"
    ]
    NUM = 27
    # private
    __id: int

    def __init__(self, note: str | int) -> None:
        if isinstance(note, Note):
            self.__id = note.__id
        elif isinstance(note, str):
            for (id, name) in enumerate(Note.NAME_LIST):
                if note == name:
                    self.__id = id
                    break
            else:
                raise ValueError(f"invalid note name: {note}")
        elif isinstance(note, int):
            if not 0 <= note <= 28:
                raise ValueError(f"expect note in [0, 28], given {note}")
            self.__id = note
        else:
            raise ValueError(f"invalid note type: {type(note)}")

    def __int__(self):
        return self.__id

    @property
    def id(self):
        return self.__id

    def __str__(self):
        return Note.NAME_LIST[self.__id]

    def __add__(self, delta: int) -> Self:
        return Note(self.__id + delta)

    def __radd__(self, delta: int) -> Self:
        return Note(self.__id + delta)

    def __sub__(self, other: Self | int) -> int | Self:
        if isinstance(other, int):
            return Note(self.__id - other)
        elif isinstance(other, Note):
            return (self.__id - other.__id)
        else:
            raise ValueError(f"invalid argument type: {type(other)}")

    def __rsub__(self, other: int | Self) -> Self | int:
        if isinstance(other, int):
            return Note(other - self.__id)
        else:
            raise ValueError(f"invalid argument type: {type(other)}")

    def __eq__(self, other: int | str | Self) -> bool:
        return self.__id == Note(other).__id


class Melody:
    """
    The melody is a simply `list` of `Note`.
    """
    __data: List[Note]

    def __init__(self, data: Sequence[Note | int | str]) -> None:
        if isinstance(data, Melody):
            self.__data = data.__data
        if isinstance(data, Sequence):
            self.__data = [Note(a) for a in data]
        else:
            raise ValueError(f"expect a sequence, given {type(data)}")

    def __len__(self) -> int:
        return len(self.__data)

    def __getitem__(self, index: int | slice) -> Note:
        return self.__data[index]

    def __str__(self) -> str:
        return str([str(note) for note in self.__data])

    @classmethod
    def cross(cls, a: Self, b: Self, index: int) -> Self:
        """
        ### Brief
        cross-over operation. 

        ### Parameter
        1. `a`, `b`: `Melody`
            Melody parents
        2. `index`: `int`
            indices, concat a[:index] and b[index:]

        Raises
        ---
        `ValueError` if type unmatched
        """
        if not isinstance(a, Melody) or not isinstance(b, Melody):
            raise ValueError(f"expected Melody: a/b, given {type(a), type(b)}")
        if not isinstance(index, int):
            raise ValueError(f"expected int: start/end, given {type(index)}")
        return Melody(a.__data[:index] + b.__data[index:])

    def transposition(self, delta: int, start: int = 0, stop: Optional[int] = None) -> None:
        if stop is None:
            stop = len(self.__data)
        for i in range(start, stop):
            if self.__data[i] != 0 and self.__data[i] != Note.NUM + 1:
                self.__data[i] += delta

    def retrograde(self, start: int = 0, stop: int = None) -> None:
        if stop is None:
            stop = len(self.__data)

        while self.__data[start] == Note.NUM + 1:
            start += 1
        while self.__data[stop] == Note.NUM + 1:
            stop += 1

        old = self.__data[start:stop]
        new = []

        i: int = 0
        j: int

        while i < len(old):
            j = i + 1
            while j < len(old) and old[j] == Note.NUM + 1:
                j += 1
            new = old[i:j] + new
            i = j

        self.__data[start:stop] = new

    def inversion(self, double_mid: int, start: int, stop: int) -> None:
        for i in range(*slice(start, stop).indices(len(self.__data))):
            if self.__data[i] != 0 and self.__data[i] != Note.NUM + 1:
                self.__data[i] = double_mid - self.__data[i]

    def mutate(self) -> None:
        # possible = [i for (i, note) in enumerate(self.__data) if note != Note.NUM + 1]
        # index = random.choice(possible)
        index = random.randint(0, len(self) - 1)
        self.__data[index] = Note(random.randint(0, Note.NUM))
