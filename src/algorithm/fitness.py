from melody import Melody, Note


def interval_score(melody: Melody) -> float:
    if len(melody) <= 1:
        return 1.0
    score = 0.0
    note_id = [note.id for note in melody if 0 <= note.id <= Note.NUM]
    for i in range(1, len(note_id)):
        interval = abs(note_id[i] - note_id[i - 1])
        if interval >= 13:  # Dissonant interval: Too large
            score += 0
        elif interval in [0, 3, 4, 5, 7, 8, 9, 12]:  # Consonant interval
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
def major_tonality_score(melody: Melody) -> float:
    pass

def minor_tonality_socre(melody: Melody) -> float:
    pass


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
    pass

