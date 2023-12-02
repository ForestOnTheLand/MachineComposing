from melody import Melody, Note
from typing import List


def interval_score(melody: Melody) -> float:
    if len(melody) <= 1:
        return 1.0
    score = 0.0
    note_id = [note.id for note in melody if 0 <= note.id <= Note.NUM]
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


def rhythm_score(melody: Melody) -> float:

    def rhythm_diff(A: List[Note], B: List[Note]) -> int:
        return sum((a.id == Note.NUM + 1) != (b.id == Note.NUM + 1) for a, b in zip(A, B))

    bars = []
    diff = 0
    for i in range(len(melody) // 8):
        bars.append(melody[i * 8:(i + 1) * 8])
    for i in range(1, len(bars)):
        diff += rhythm_diff(bars[i - 1], bars[i])
    return 1 - diff / (8 * len(bars))
