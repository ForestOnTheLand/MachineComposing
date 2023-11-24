from typing import List, Iterable


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
        if isinstance(note, str):
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

    def __str__(self):
        return Note.NAME_LIST[self.__id]


class Melody:
    """
    The melody is a simply `list` of `Note`.
    """
    __melody: List[Note]

    def __init__(self, data: Iterable[Note | int | str]) -> None:
        if isinstance(data, Iterable):
            self.__melody = [Note(a) for a in data]
        else:
            raise ValueError(f"expect a list, given {type(data)}")

    def __len__(self) -> int:
        return len(self.__melody)

    def __getitem__(self, index: int) -> Note:
        return self.__melody[index]
