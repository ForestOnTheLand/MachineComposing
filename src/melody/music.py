from typing import List, Sequence, Optional, overload, Iterator, Tuple
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
                raise ValueError(f"Invalid note name: {note}")
        elif isinstance(note, int):
            if not 0 <= note <= 28:
                raise ValueError(f"Expect note in [0, 28], given {note}")
            self.__id = note
        else:
            raise ValueError(f"Can not convert {type(note)} to note")

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, id: int) -> None:
        if not isinstance(id, int):
            raise ValueError(f"Expected int, given {type(id)}")
        if not 0 <= id <= Note.NUM + 1:
            raise ValueError(f"Expect note in [0, 28], given {id}")
        self.__id = id

    def __str__(self):
        return Note.NAME_LIST[self.__id]

    def __add__(self, delta: int) -> 'Note':
        if not isinstance(delta, int):
            raise ValueError(f"expected int, given {type(delta)}")
        return Note(self.__id + delta)

    def __iadd__(self, delta: int) -> Self:
        if not isinstance(delta, int):
            raise ValueError(f"expected int, given {type(delta)}")
        self.__id += delta
        return self

    def __radd__(self, delta: int) -> 'Note':
        if not isinstance(delta, int):
            raise ValueError(f"expected int, given {type(delta)}")
        return Note(self.__id + delta)

    def __sub__(self, other: int) -> 'Note':
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
            raise ValueError(f"Can not convert {type(data)} to melody")

    def pad_or_cut_to(self, length: int) -> 'Melody':
        from math import ceil
        if length <= len(self):
            return Melody(self[:length])
        else:
            return Melody((self.__data * ceil(length / len(self)))[:length])

    def __iter__(self) -> Iterator[Note]:
        return iter(self.__data)

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


class Tonality:
    """
        The tonality is s set of notes
    """
    Note_List: List[int]

    MODES = {"major": [2, 2, 1, 2, 2, 2, 1], "minor": [2, 1, 2, 2, 1, 2, 2]}

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
        return all(note in self.Note_List for note in melody)
        # return False not in [note in self.Note_List for note in melody]

    def fitness(self, melody: Melody) -> float:
        return sum([note in self.Note_List for note in melody]) / len(melody)

    def __len__(self):
        return len(self.Note_List)


TONALITY = {
    "major": {
        'C': [1, 3, 5, 7, 8, 10, 12, 13, 15, 17, 19, 20, 22, 24, 25, 27],
        '#C': [1, 2, 4, 6, 8, 9, 11, 13, 14, 16, 18, 20, 21, 23, 25, 26],
        'D': [2, 3, 5, 7, 9, 10, 12, 14, 15, 17, 19, 21, 22, 24, 26, 27],
        '#D': [1, 3, 4, 6, 8, 10, 11, 13, 15, 16, 18, 20, 22, 23, 25, 27],
        'E': [2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19, 21, 23, 24, 26],
        'F': [1, 3, 5, 6, 8, 10, 12, 13, 15, 17, 18, 20, 22, 24, 25, 27],
        '#F': [1, 2, 4, 6, 7, 9, 11, 13, 14, 16, 18, 19, 21, 23, 25, 26],
        'G': [2, 3, 5, 7, 8, 10, 12, 14, 15, 17, 19, 20, 22, 24, 26, 27],
        '#G': [1, 3, 4, 6, 8, 9, 11, 13, 15, 16, 18, 20, 21, 23, 25, 27],
        'A': [2, 4, 5, 7, 9, 10, 12, 14, 16, 17, 19, 21, 22, 24, 26],
        '#A': [1, 3, 5, 6, 8, 10, 11, 13, 15, 17, 18, 20, 22, 23, 25, 27],
        'B': [2, 4, 6, 7, 9, 11, 12, 14, 16, 18, 19, 21, 23, 24, 26],
    },
    "minor": {
        'C': [1, 3, 4, 6, 8, 10, 11, 13, 15, 16, 18, 20, 22, 23, 25, 27],
        '#C': [2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19, 21, 23, 24, 26],
        'D': [1, 3, 5, 6, 8, 10, 12, 13, 15, 17, 18, 20, 22, 24, 25, 27],
        '#D': [1, 2, 4, 6, 7, 9, 11, 13, 14, 16, 18, 19, 21, 23, 25, 26],
        'E': [2, 3, 5, 7, 8, 10, 12, 14, 15, 17, 19, 20, 22, 24, 26, 27],
        'F': [1, 3, 4, 6, 8, 9, 11, 13, 15, 16, 18, 20, 21, 23, 25, 27],
        '#F': [2, 4, 5, 7, 9, 10, 12, 14, 16, 17, 19, 21, 22, 24, 26],
        'G': [1, 3, 5, 6, 8, 10, 11, 13, 15, 17, 18, 20, 22, 23, 25, 27],
        '#G': [2, 4, 6, 7, 9, 11, 12, 14, 16, 18, 19, 21, 23, 24, 26],
        'A': [1, 3, 5, 7, 8, 10, 12, 13, 15, 17, 19, 20, 22, 24, 25, 27],
        '#A': [1, 2, 4, 6, 8, 9, 11, 13, 14, 16, 18, 20, 21, 23, 25, 26],
        'B': [2, 3, 5, 7, 9, 10, 12, 14, 15, 17, 19, 21, 22, 24, 26, 27]
    },
    "harmonic": {
        'C': [1, 3, 4, 7, 8, 10, 11, 13, 15, 16, 19, 20, 22, 23, 25, 27],
        '#C': [2, 4, 5, 8, 9, 11, 12, 14, 16, 17, 20, 21, 23, 24, 26],
        'D': [1, 3, 5, 6, 9, 10, 12, 13, 15, 17, 18, 21, 22, 24, 25, 27],
        '#D': [1, 2, 4, 6, 7, 10, 11, 13, 14, 16, 18, 19, 22, 23, 25, 26],
        'E': [2, 3, 5, 7, 8, 11, 12, 14, 15, 17, 19, 20, 23, 24, 26, 27],
        'F': [1, 3, 4, 6, 8, 9, 12, 13, 15, 16, 18, 20, 21, 24, 25, 27],
        '#F': [1, 2, 4, 5, 7, 9, 10, 13, 14, 16, 17, 19, 21, 22, 25, 26],
        'G': [2, 3, 5, 6, 8, 10, 11, 14, 15, 17, 18, 20, 22, 23, 26, 27],
        '#G': [3, 4, 6, 7, 9, 11, 12, 15, 16, 18, 19, 21, 23, 24, 27],
        'A': [1, 4, 5, 7, 8, 10, 12, 13, 16, 17, 19, 20, 22, 24, 25],
        '#A': [1, 2, 5, 6, 8, 9, 11, 13, 14, 17, 18, 20, 21, 23, 25, 26],
        'B': [2, 3, 6, 7, 9, 10, 12, 14, 15, 18, 19, 21, 22, 24, 26, 27],
    },
    "melodic": {
        'C': [1, 3, 5, 7, 8, 10, 11, 13, 15, 17, 19, 20, 22, 23, 25, 27],
        '#C': [2, 4, 6, 8, 9, 11, 12, 14, 16, 18, 20, 21, 23, 24, 26],
        'D': [1, 3, 5, 7, 9, 10, 12, 13, 15, 17, 19, 21, 22, 24, 25, 27],
        '#D': [1, 2, 4, 6, 8, 10, 11, 13, 14, 16, 18, 20, 22, 23, 25, 26],
        'E': [2, 3, 5, 7, 9, 11, 12, 14, 15, 17, 19, 21, 23, 24, 26, 27],
        'F': [1, 3, 4, 6, 8, 10, 12, 13, 15, 16, 18, 20, 22, 24, 25, 27],
        '#F': [1, 2, 4, 5, 7, 9, 11, 13, 14, 16, 17, 19, 21, 23, 25, 26],
        'G': [2, 3, 5, 6, 8, 10, 12, 14, 15, 17, 18, 20, 22, 24, 26, 27],
        '#G': [1, 3, 4, 6, 7, 9, 11, 13, 15, 16, 18, 19, 21, 23, 25, 27],
        'A': [2, 4, 5, 7, 8, 10, 12, 14, 16, 17, 19, 20, 22, 24, 26],
        '#A': [1, 3, 5, 6, 8, 9, 11, 13, 15, 17, 18, 20, 21, 23, 25, 27],
        'B': [2, 4, 6, 7, 9, 10, 12, 14, 16, 18, 19, 21, 22, 24, 26],
    },
    "five":{
        'C':[3, 5, 8, 10, 12, 15, 17, 20, 22, 24],
        '#C':[1, 4, 6, 9, 11, 13, 16, 18, 21, 23, 25],
        'D':[2, 5, 7, 10, 12, 14, 17, 19, 22, 24, 26],
        '#D':[1, 3, 6, 8, 11, 13, 15, 18, 20, 23, 25, 27],
        'E':[2, 4, 7, 9, 12, 14, 16, 19, 21, 24, 26],
        'F':[1, 3, 5, 8, 10, 13, 15, 17, 20, 22, 25, 27],
        '#F':[2, 4, 6, 9, 11, 14, 16, 18, 21, 23, 26],
        'G':[3, 5, 7, 10, 12, 15, 17, 19, 22, 24],
        '#G':[1, 4, 6, 8, 11, 13, 16, 18, 20, 23, 25],
        'A':[2, 5, 7, 9, 12, 14, 17, 19, 21, 24, 26],
        '#A':[1, 3, 6, 8, 10, 13, 15, 18, 20, 22, 25],
        'B':[2, 4, 7, 9, 11, 14, 16, 19, 21, 23, 26],
    }
}


def get_tonality(melody: Melody, mode: List[str] | str) -> Tuple[float, str | None]:
    """
    mode: str or List[str], such as "major", "minor", "C harmonic", "#A major", ...
    """

    tonalities = {}

    def parse_mode(s: str) -> None:
        if not isinstance(s, str):
            raise ValueError(f"Expected mode: str | List[str], given {type(mode)}")
        splited = s.split()
        try:
            if len(splited) == 1:
                for key, val in TONALITY[splited[0]].items():
                    tonalities[key + ' ' + splited[0]] = val
            elif len(splited) == 2:
                tonic, m = splited
                tonalities[tonic + ' ' + m] = TONALITY[m][tonic]
            else:
                raise ValueError(f"Unknown mode {s}")
        except KeyError:
            raise ValueError(f"Unknown mode {s}")

    if isinstance(mode, list):
        for s in mode:
            parse_mode(s)
    elif isinstance(mode, str):
        parse_mode(mode)
    else:
        raise ValueError(f"Expected mode: str | List[str], given {type(mode)}")

    best_count: int = 0  # The number of notes in tonality
    best_mode: str | None = None  # The style of melody
    note_id: List[int] = [note.id for note in melody if 1 <= note.id <= Note.NUM]
    if not note_id:
        return 0.0, None

    for key, note_list in tonalities.items():
        count = sum(note in note_list for note in note_id)
        if count > best_count:
            best_count, best_mode = count, key

    return best_count / len(note_id), best_mode


# 0: Stable, 1: Unstable, 2: Very-Unstable, 3: Not-in-Tonality
STABILITY = [0, 3, 1, 3, 0, 2, 3, 0, 3, 1, 3, 2]


def get_stability(note: int, main_note: int) -> int:
    return 3 if note in [0, Note.NUM + 1] else STABILITY[(note - main_note) % 12]
