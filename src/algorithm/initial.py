from melody import Melody, Note
import random


class RandomGenerator:

    def __init__(self, length: int = 32) -> None:
        self.length = length

    def __call__(self) -> Melody:
        melody = []
        while len(melody) < self.length:
            melody.append(random.randint(0, Note.NUM))
            melody += [Note.NUM + 1] * random.randint(0, 3)
        return Melody(melody[:self.length])
