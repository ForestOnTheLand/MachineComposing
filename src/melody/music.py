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
        "0", "F3", "#F3", "G3", "#G3", "A3", "#A3", "B3", "C4", "#C4", "D4", "#D4", "E4", "F4",
        "#F4", "G4", "#G4", "A4", "#A4", "B4", "C5", "#C5", "D5", "#D5", "E5", "F5", "#F5", "G5",
        "-"
    ]
    NUM = 27
    # private
    __id: int

    def __init__(self, note: Self | str | int) -> None:
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

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, id: int) -> None:
        if not isinstance(id, int):
            raise ValueError(f"expected int, given {type(id)}")
        if not 0 <= id <= Note.NUM + 1:
            raise ValueError(f"expect note in [0, 28], given {id}")
        self.__id = id

    def __str__(self):
        return Note.NAME_LIST[self.__id]

    def __add__(self, delta: int) -> Self:
        if not isinstance(delta, int):
            raise ValueError(f"expected int, given {type(delta)}")
        return Note(self.__id + delta)

    def __iadd__(self, delta: int) -> Self:
        if not isinstance(delta, int):
            raise ValueError(f"expected int, given {type(delta)}")
        self.__id += delta
        return self

    def __radd__(self, delta: int) -> Self:
        if not isinstance(delta, int):
            raise ValueError(f"expected int, given {type(delta)}")
        return Note(self.__id + delta)

    def __sub__(self, other: int) -> Self:
        if isinstance(other, int):
            return Note(self.__id - other)
        else:
            raise ValueError(f"invalid argument type: {type(other)}")

    def __eq__(self, other: str | int | Self):
        if isinstance(other, Note):
            return self.id == other.id
        elif isinstance(other, int):
            return self.id == other
        elif isinstance(other, str):
            return self.NAME_LIST[self.id] == other
        else:
            raise ValueError(f"invalid argument type: {type(other)}")


class Melody:
    """
    The melody is a simply `list` of `Note`.
    """
    __data: List[Note]

    def __init__(self, data: Self | Sequence[Note | int | str]) -> None:
        if isinstance(data, (Melody, Sequence)):
            self.__data = [Note(a) for a in data]
        else:
            raise ValueError(f"expect a sequence, given {type(data)}")

    def __len__(self) -> int:
        return len(self.__data)

    @overload
    def __getitem__(self, index: int) -> Note:
        ...

    @overload
    def __getitem__(self, index: slice) -> List[Note]:
        ...

    def __getitem__(self, index: int | slice) -> Note | List[Note]:
        return self.__data[index]

    @overload
    def __setitem__(self, index: int, value: Note) -> None:
        ...

    @overload
    def __setitem__(self, index: slice, value: List[Note]) -> None:
        ...

    def __setitem__(self, index: int | slice, value: Note | List[Note]) -> None:
        if isinstance(index, int) and isinstance(value, Note):
            self.__data[index] = value
        elif isinstance(index, slice) and isinstance(value, list):
            for i, val in zip(range(*index.indices(len(self.__data))), value):
                self.__data[i] = val

    def __str__(self) -> str:
        return str([str(note) for note in self.__data])

    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, Melody):
            raise ValueError(f"expected Melody, given {type(other)}")
        return all(a.id == b.id for a, b in zip(self.__data, other.__data))

    # TODO: The following functions should be put in algorithm.operation later!
    # Some might be buggy

    # def transposition(self, delta: int, start: int = 0, stop: Optional[int] = None) -> None:
    #     if stop is None:
    #         stop = len(self.__data)
    #     for i in range(start, stop):
    #         if self.__data[i] != 0 and self.__data[i] != Note.NUM + 1:
    #             self.__data[i] += delta

    # def retrograde(self, start: int = 0, stop: Optional[int] = None) -> None:
    #     if stop is None:
    #         stop = len(self.__data)

    #     while self.__data[start] == Note.NUM + 1:
    #         start += 1
    #     while self.__data[stop] == Note.NUM + 1:
    #         stop += 1

    #     old = self.__data[start:stop]
    #     new = []

    #     i: int = 0
    #     j: int

    #     while i < len(old):
    #         j = i + 1
    #         while j < len(old) and old[j] == Note.NUM + 1:
    #             j += 1
    #         new = old[i:j] + new
    #         i = j

    #     self.__data[start:stop] = new

    # def inversion(self, s: int, start: Optional[int] = None, stop: Optional[int] = None) -> None:
    #     for i in range(*slice(start, stop).indices(len(self.__data))):
    #         if self.__data[i].id != 0 and self.__data[i].id != Note.NUM + 1:
    #             self.__data[i] = Note(s - self.__data[i].id)


class Tonality:
    """
        The tonality is s set of notes
    """
    Note_List: List[int]

    MODES = {
        "major": [2, 2, 1, 2, 2, 2, 1],
        "minor": [2, 1, 2, 2, 1, 2, 2]
    }

    def __init__(self, principal_note: Note | str | int, mode: str):

        if mode not in Tonality.MODES.keys():
            print(f"invalid mode : {mode}")
        principal_note = Note(principal_note)
        if principal_note.id <= 0 or principal_note.id > Note.NUM:
            print(f"invalid note : {principal_note.NAME_LIST[principal_note.id]}")

        mode_len = len(Tonality.MODES[mode])

        note_id = principal_note.id
        k = mode_len - 1
        self.Note_List = []
        while note_id > 0:
            self.Note_List.append(note_id)
            note_id -= Tonality.MODES[mode][k]
            k = (k + mode_len - 1) % mode_len
        note_id = principal_note.id + Tonality.MODES[mode][0]
        k = 1
        while note_id <= Note.NUM:
            self.Note_List.append(note_id)
            note_id += Tonality.MODES[mode][k]
            k = (k + 1) % mode_len
            k = (k + 1) % mode_len

    def __iter__(self):
        return iter([Note(i) for i in self.Note_List])

    def harmony(self, melody: Melody) -> bool:
        return False not in [note in self.Note_List for note in melody]

    def fitness(self, melody: Melody) -> float:
        return sum([note in self.Note_List for note in melody]) / len(melody)

    def __len__(self):
        return len(self.Note_List)
