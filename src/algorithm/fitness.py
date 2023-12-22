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

from melody import Melody, Note, Tonality, TONALITY, STABILITY, get_stability, get_tonality
from typing import List, Tuple, Dict, Callable

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
        elif interval in [0, 2, 3, 4, 7, 8, 9]:  # Consonant interval
            score += 1
        else:
            score += 0.5
    return score / (len(note_id) - 1)


"""
    寻找与旋律最相近的大/小调
    返回旋律中调内音的比例
"""


def tonality_score(melody: Melody, mode: List[str] | str) -> float:
    return get_tonality(melody, mode)[0]


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
    return ratio


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
    if len(melody) <= 1:
        return 1.0
    score = 0.0
    note_id = [note.id for note in melody if 1 <= note.id <= Note.NUM]
    best_mode = get_tonality(melody, mode='major')[1].split(' ')[0]
    main_note = Note(best_mode + '4').id

    last_stability = -1
    stable_position = []
    for index in range(len(note_id)):
        note = note_id[index]
        stability = get_stability(note, main_note)
        if stability == 0 and last_stability != 0:
            stable_position.append(index)
        if stability != 3:
            last_stability = stability

    count = 0
    for index in range(1, len(stable_position)):
        if (stable_position[index] - stable_position[index - 1] < 4):
            count += 1

    if len(stable_position) > 1:
        score = count / (len(stable_position))
    else:
        score = 0.0
    return score


"""
判断旋律是否以稳定音开始、以稳定音结束
均符合返回1,一端符合返回0.5,均不符合返回0
"""


def boundary_score(melody: Melody) -> float:
    if len(melody) <= 1:
        return 1.0
    note_id = [note.id for note in melody if 1 <= note.id <= Note.NUM]
    best_mode = get_tonality(melody, mode='major')[1].split(' ')[0]
    main_note = Note(best_mode + '4').id
    return ((get_stability(note_id[0], main_note) == 0) +
            (get_stability(note_id[-1], main_note) == 0)) / 2


# Penalty functions


def density_penalty(
        melody: Melody,
        thresholds: Tuple[float, float, float, float] = (1.0, 0.875, 0.5, 0.3125),
) -> float:
    """Avoid melody with extremely low/high density.

    Parameters
    ----------
    `melody` : `Melody`
        melody to evaluate
    `thresholds` : Tuple[float, float, float, float]
        Represents (max_threshold, upper_threshold, lower_threshold, min_threshold).
        By default (1.0, 0.875, 0.5, 0.3125).
    
    Returns
    -------
    `float`
        Penalty in [0.0, 1.0]. 
        0.0 for densities in range [lower_threshold, upper_threshold];
        1.0 for densities not in range (min_threshold, max_threshold);
        and linear penalty in other ranges.
    """
    note_num = sum(1 <= note.id <= Note.NUM for note in melody)
    density = note_num / len(melody)

    max_threshold, upper_threshold, lower_threshold, min_threshold = thresholds

    if not 0 <= min_threshold <= lower_threshold < upper_threshold <= max_threshold <= 1:
        raise ValueError(f"Invalid thresholds: {thresholds}")

    if density > max_threshold:
        return 1.0
    elif density > upper_threshold:
        return (density - upper_threshold) / (max_threshold - upper_threshold)
    elif density > lower_threshold:
        return 0.0
    elif density > min_threshold:
        return (lower_threshold - density) / (lower_threshold - min_threshold)
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


def rest_penalty(melody: Melody) -> float:
    """Avoid any rest in melody.
    
    Parameters
    ----------
    `melody` : `Melody`
        melody to evaluate
    
    Returns
    -------
    `float`
        0.0 for melody without rest('0'), 1.0 for others.
    """
    return 1.0 if any(note.id == 0 for note in melody) else 0.0


def consecutive_penalty(melody: Melody, threshold: int = 8) -> float:
    """Avoid too many consecutive eight notes (more than a given threshold).
    
    Parameters
    ----------
    `melody` : `Melody`
        melody to evaluate
    `threshold` : `int`, optional
        Any melody with more than <threshold> eight notes is unacceptable.
        By default `8`.
    
    Returns
    -------
    `float`
        1.0 for melody with more than <threshold> eight notes, 0.0 otherwise.
    """
    if not isinstance(threshold, int):
        raise ValueError(f"Expected threshold: int, given {type(threshold)}")
    if threshold <= 0:
        raise ValueError(f"Expected threshold > 0, given {threshold}")

    length = threshold + 1
    for i in range(len(melody) - length):
        if all(1 <= note.id <= Note.NUM for note in melody[i:i + length]):
            return 1.0
    return 0.0


def range_penalty(melody: Melody, threshold: int) -> float:

    def get_range(melody: Melody) -> int:
        minp, maxp = Note.NUM, 1
        for note in melody:
            if note.id != 0 and note.id != Note.NUM + 1:
                minp = min(minp, note.id)
                maxp = max(maxp, note.id)
        diff = maxp - minp
        return diff if diff >= 0 else Note.NUM

    return 1.0 if get_range(melody) > threshold else 0.0


def variety_penalty(melody: Melody, threshold: int) -> float:
    record = [0] * (Note.NUM + 2)
    for note in melody:
        record[note.id] = 1
    variety = sum(record[1:-1])
    return 1.0 if variety < threshold else 0.0
