from melody import Melody, Note
from typing import Tuple, List, Sequence, Optional
import random
import util


def one_point_cross(a: Melody, b: Melody, index: int) -> Melody:
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
        raise ValueError(f"expected int: index, given {type(index)}")
    return Melody(a[:index] + b[index:])


def two_points_cross(a: Melody, b: Melody, indices: Tuple[int, int]) -> Melody:
    """
    ### Brief
    cross-over operation. 

    ### Parameter
    1. `a`, `b`: `Melody`
        Melody parents
    2. `indices`: `int`
        indices, concat a[:left] + b[left:right] + a[right:]

    Raises
    ---
    `ValueError` if type unmatched
    """
    if not isinstance(a, Melody) or not isinstance(b, Melody):
        raise ValueError(f"expected Melody: a/b, given {type(a), type(b)}")
    left, right = indices
    if not isinstance(left, int) or not isinstance(right, int):
        raise ValueError(f"expected ints: indices, given {type(left), type(right)}")
    return Melody(a[:left] + b[left:right] + a[right:])


def one_point_mutate(
    melody: Melody,
    index: Optional[int] = None,
    *,
    note_list: Sequence = Note.NAME_LIST,
) -> None:
    if index is None:
        index = random.randint(0, len(melody) - 1)
    note = Note(random.choice(note_list))
    if note.id != Note.NUM + 1 or index != 0:
        melody[index] = note


def max_note(melody: Melody | List[Note]) -> int:
    result = 0
    for note in melody:
        if note.id not in [0, Note.NUM + 1]:
            result = max(note.id, result)
    return result


def min_note(melody: Melody | List[Note]) -> int:
    result = Note.NUM + 1
    for note in melody:
        if note.id not in [0, Note.NUM + 1]:
            result = min(note.id, result)
    return result


def transpose(
    melody: Melody,
    delta: None | int = None,
    indices: None | Tuple[int, int | None] = None,
) -> None:
    """
    Transpose `melody[indices[0]:indices[1]]` by `delta`.
    If not given, `delta` will be selected randomly among all valid values.
    """
    if indices is None:
        indices = util.random_interval(len(melody))
    start, stop = indices
    notes = melody[start:stop]
    if delta is None:
        delta = random.randint(1 - min_note(notes), Note.NUM - max_note(notes))
    for note in notes:
        if note.id not in [0, Note.NUM + 1]:
            note.id += delta


def retrograde(
    melody: Melody,
    indices: None | Tuple[int, int | None] = None,
) -> None:
    if indices is None:
        indices = util.random_interval(len(melody))
    start, stop = indices
    if stop is None:
        stop = len(melody) - 1
    if start == stop:
        return
    while melody[start].id == Note.NUM + 1:
        start -= 1
    while stop < len(melody) and melody[stop].id == Note.NUM + 1:
        stop += 1

    old_notes = melody[start:stop]
    new_notes = []
    i: int = 0
    j: int
    while i < stop:
        j = i + 1
        while j < len(old_notes) and old_notes[j].id == Note.NUM + 1:
            j += 1
        new_notes = old_notes[i:j] + new_notes
        i = j

    melody[start:stop] = new_notes


def inverse(
    melody: Melody,
    s: Optional[int] = None,
    indices: None | Tuple[int, int | None] = None,
) -> None:
    """
    Inverse `melody[indices[0]:indices[1]]` by changing `note` to `Note(s - note.id)`.
    If not given, `s` will be selected randomly among all valid values.
    """
    if indices is None:
        indices = util.random_interval(len(melody))
    start, stop = indices
    notes = melody[start:stop]
    if s is None:
        s = random.randint(max_note(notes) + 1, min_note(notes) + Note.NUM)
    for note in notes:
        if note.id not in [0, Note.NUM + 1]:
            note.id = s - note.id
