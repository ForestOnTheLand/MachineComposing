"""
Basically, there are 2 kinds of functions:

xxx_score: Evaluate most individuals.
    Ranging from [0.0, 1.0]. The larger, the better.
    This value should varies for all individuals.
    Those functions determine the direction of evolution.

xxx_penalty: Specially punish extremely bad individuals.
    Ranging from [0.0, 1.0]. The smaller, the better. 
    For most individuals (i.e. not too bad), this value should be 0.0, so this score doesn't count.
    But for extremely bad ones, this value should be larger.
    Those functions DO NOT determine the direction of evolution. They only avoid bad individuals.

"""

from melody import Melody, Note, Tonality, TONALITY
from typing import List

# Score functions


def interval_score(melody: Melody) -> float:
    if len(melody) <= 1:
        return 1.0
    score = 0.0
    note_id = [note.id for note in melody if 1 <= note.id <= Note.NUM]
    if len(note_id) <= 1:
        return 0
    for i in range(1, len(note_id)):
        interval = abs(note_id[i] - note_id[i - 1])
        if interval >= 13:  # Dissonant interval: Too large
            score += 0
        elif interval in [0, 3, 4, 5, 7, 8, 9]:  # Consonant interval
            score += 1
        else:
            score += 0.5
    return score / (len(note_id) - 1)
    # return score / (len(melody) - 1)


def variety_score(melody: Melody) -> float:
    record = [0 for _ in range(Note.NUM + 2)]
    for note in melody:
        record[note.id] = 1
    return min(2 * sum(record) / Note.NUM, 1.0)


"""
    寻找与旋律最相近的大/小调
    返回旋律中调内音的比例
"""


def tonality_score(melody: Melody, mode: str) -> float:
    if mode not in TONALITY.keys():
        raise ValueError(f"Invalid mode: {mode}, expected in {list(TONALITY.keys())}")
    count = 0  # The number of notes in tonality
    note_id = [note.id for note in melody if 1 <= note.id <= Note.NUM]
    for note_list in TONALITY["major"].values():
        count = max(count, sum(note in note_list for note in note_id))
    if len(note_id) == 0:
        return 0.0
    return count / len(note_id)


"""
    采用现代旋律创作中的"稳定-不稳定-稳定"理论
    在大调式中，将主和弦的三个音视为稳定音
    二、六音视为较不稳定音
    四、七音视为极不稳定音
    有下列要求：
        旋律以稳定音起始与结束
        旋律在进行的过程中需要不稳定音的参与
        旋律允许的变化如下：
            稳定 - 较不稳定 - 稳定
            稳定 - 极不稳定 - 稳定
            稳定 - 较不稳定 - 极不稳定 - 稳定
            稳定 - 极不稳定 - 较不稳定 - 稳定
            
    函数返回对于此理论的符合程度，返回值在[0,1]
"""


def stable_score(melody: Melody) -> float:
    ...


def rhythm_score(melody: Melody) -> float:
    """This function works bad. Be careful.
    """

    def rhythm_diff(A: List[Note], B: List[Note]) -> int:
        return sum((a.id == Note.NUM + 1) != (b.id == Note.NUM + 1) for a, b in zip(A, B))

    bars = []
    diff = 0
    for i in range(len(melody) // 8):
        bars.append(melody[i * 8:(i + 1) * 8])
    for i in range(1, len(bars)):
        diff += rhythm_diff(bars[i - 1], bars[i])
    ratio = 1 - diff / (8 * len(bars))
    return min(ratio / 0.9, 1.0)


# Penalty functions


def density_penalty(melody: Melody) -> float:
    """Avoid melody with extremely low/high density.

    Parameters
    ----------
    `melody` : `Melody`
        melody to evaluate
    
    Returns
    -------
    `float`
        Penalty in [0.0, 1.0]. 0.0 for most melodies, but a non-zero value for
        melodies with extremely low/high density.
    """
    note_num = sum(1 <= note.id <= Note.NUM for note in melody)
    density = note_num / len(melody)
    if density > 7 / 8:
        return (density - 7 / 8) / (1 - 7 / 8)
    elif density > 16 / 32:
        return 0.0
    elif density > 10 / 32:
        return ((16 / 32) - density) / ((16 / 32) - (10 / 32))
    else:
        return 1.0


def stop_penalty(melody: Melody) -> float:
    """Avoid melody with immediate stop at the end.

    Parameters
    ----------
    `melody` : `Melody`
        melody to evaluate
    
    Returns
    -------
    `float`
        Penalty in [0.0, 1.0]. 1.0 for melodies with a note at the end, and 0.0 for others.
    """
    return 1.0 if 0 <= melody[-1].id <= Note.NUM else 0.0
