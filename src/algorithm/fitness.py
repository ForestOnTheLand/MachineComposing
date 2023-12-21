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
from typing import List, Tuple

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


def variety_score(melody: Melody) -> float:
    record = [0 for _ in range(Note.NUM + 2)]
    for note in melody:
        record[note.id] = 1
    return min(2 * sum(record) / Note.NUM, 1.0)


"""
    寻找与旋律最相近的大/小调
    返回旋律中调内音的比例
"""


def get_tonality(melody: Melody, mode: List[str] | str) -> Tuple[float, None | str]:
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


def tonality_score(melody: Melody, mode: List[str] | str) -> float:
    return get_tonality(melody, mode)[0]


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
    mode2note = {'C' : 8,
                     '#C' : 9,
                     'D' : 10,
                     '#D' : 11,
                     'E' : 12,
                     'F' : 13,
                     '#F' : 14,
                     'G' : 15,
                     '#G' : 16,
                     'A' : 17,
                     '#A' : 18,
                     'B' : 19}
    if len(melody) <= 1:
        return 1.0
    score = 0.0
    note_id = [note.id for note in melody if 1 <= note.id <= Note.NUM]
    best_mode = get_tonality(melody, mode='major')[1].split(' ')[0]
    main_note = mode2note[best_mode]
    stable_notes = [main_note]
    unstable_notes = []
    very_unstable_notes = []
    i = main_note
    while (i < 28):
        if (i + 2 < 28):
            unstable_notes.append(i+2)
        if (i + 4 < 28):
            stable_notes.append(i+4)
        if (i + 5 < 28):
            very_unstable_notes.append(i+5)
        if (i + 7 < 28):
            stable_notes.append(i+7)
        if (i + 9 < 28):
            unstable_notes.append(i+9)
        if (i + 11 < 28):
            very_unstable_notes.append(i+11)
        if (i + 12 < 28):
            stable_notes.append(i+12)
        i = i + 12
    while (i > 0):
        if (i - 1 > 0):
            very_unstable_notes.append(i-1)
        if (i - 3 > 0):
            unstable_notes.append(i-3)
        if (i - 5 > 0):
            stable_notes.append(i-4)
        if (i - 7 > 0):
            very_unstable_notes.append(i-7)
        if (i - 8 > 0):
            stable_notes.append(i-8)
        if (i - 10 > 0):
            unstable_notes.append(i-10)
        if (i - 12 > 0):
            stable_notes.append(i-12)
        i = i - 12
    notes = [-1]
    stable_position = []
    for index in range(len(note_id)):
        note = note_id[index]
        if ((note in stable_notes) and (notes[len(notes)-1] != 0)):
            notes.append(0)
            stable_position.append(index)
        elif ((note in unstable_notes) and (notes[len(notes)-1] != 1)):
            notes.append(1)
        elif ((note in very_unstable_notes) and (notes[len(notes)-1] != 2)):
            notes.append(2)
    count = 0
    for index in range(1, len(stable_position)):
        if (stable_position[index] - stable_position[index-1] < 4):
            count += 1
    if (len(stable_position) > 1):
        score = count/(len(stable_position))
    else:
        score = 0
    return score


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
