from melody import Melody, Note
import random
from typing import Sequence


class RandomGenerator:

    def __init__(self, length: int = 32, name_list: Sequence = Note.NAME_LIST[:-1]) -> None:
        self.length = length
        self.name_list = name_list

    def __call__(self) -> Melody:
        melody = []
        while len(melody) < self.length:
            melody.append(random.choice(self.name_list))
            melody += [Note.NUM + 1] * random.randint(0, 3)
        return Melody(melody[:self.length])
