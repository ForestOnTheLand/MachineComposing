from melody import Melody, Note


def cross(a: Melody, b: Melody, index: int) -> Melody:
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
