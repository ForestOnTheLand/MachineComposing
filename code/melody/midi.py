import pygame
from mido import Message, MidiFile, MidiTrack
from typing import List
from .music import Note, Melody


def save_midi(
    melody: Melody,
    path: str,
    *,
    instrument: int = 0,
    velocity: int | float = 100,
    time: int | float = 240,
) -> None:
    """
    ### Parameters
    1. `melody`: `Melody`
        See class `Melody` and `Note` for more detailed information.
    2. `path`: `str`
        Path of output file
    3. `instrument`: `int`, default: 0 (Acoustic Grand Piano).
        Instrument type, from 0 to 127. 
        See https://blog.csdn.net/ruyulin/article/details/84103186 for more details

    Raises
    ---
    `ValueError` if begin with a prolongation note.
    """

    if not isinstance(melody, Melody):
        melody = Melody(melody)

    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(Message('program_change', program=instrument))

    length: int = len(melody)
    i: int = 0
    pause: int = 0
    while i < length:
        if int(melody[i]) == 0:
            pause += 1
            i += 1
            while i < length and int(melody[i]) == Note.NUM + 1:
                pause += 1
                i += 1
        elif 1 <= int(melody[i]) <= Note.NUM:
            note: int = int(melody[i]) + 52
            duration: int = 1
            i += 1
            while i < length and int(melody[i]) == Note.NUM + 1:
                duration += 1
                i += 1
            track.append(Message('note_on', note=note, velocity=velocity, time=time * pause))
            track.append(Message('note_off', note=note, velocity=velocity, time=time * duration))
            pause = 0
        else:
            raise ValueError(f"argument melody: invalid melody[{i}] = {melody[i]}")

    mid.save(path)


def play_midi(path: str, *, volume: float = 1.0) -> None:
    """
    ### Parameters
    1. `path`: `str`
        Path of input file
    2. `volume`: `int`. default: 1
        Volume of music, ranging from 0.0 to 1.0.
        Any number larger than 1.0 will be considered as 1.0
    """
    pygame.mixer.init()
    clock = pygame.time.Clock()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(volume)
    while pygame.mixer.music.get_busy():
        clock.tick(30)
