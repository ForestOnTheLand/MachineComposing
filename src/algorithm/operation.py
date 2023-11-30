from melody import Melody, Note
from typing import Tuple
import random


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


def one_point_mutate(melody: Melody, index: int) -> None:
    melody[index] = Note(random.randint(0, Note.NUM))
