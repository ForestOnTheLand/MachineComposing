import os, sys

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = ""

import pygame
from mido import Message, MidiFile, MidiTrack
from typing import List

NOTES = 27


def save_midi(
    melody: List[int],
    path: str,
    *,
    instrument: int = 0,
    velocity: int | float = 100,
    time: int | float = 240,
) -> None:
    """
    ### Parameters
    1. `melody`: `List[int]`
        As is described in the paper, the melody is a `list` of `int`, ranging from
        `0`(included) to `28`(included). `0` stands for a break, `28` for a prolongation,
        and other numbers from `1` to `27` represents notes from F3(53) to G5(79) respectively.
    2. `path`: `str`
        Path of output file
    3. `instrument`: `int`, default: 0 (Acoustic Grand Piano).
        Instrument type, from 0 to 127. 
        See https://blog.csdn.net/ruyulin/article/details/84103186 for more details.

    Raises
    ---
    `ValueError` if melody is empty or begin with 28.
    """

    if not isinstance(melody, list):
        raise ValueError(f"argument melody: {type(melody)}, expected list")
    if len(melody) == 0:
        raise ValueError("argument melody: empty list")
    if melody[0] == NOTES + 1:
        raise ValueError(f"argument melody: shouldn't begin with {NOTES + 1}")

    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(Message('program_change', program=instrument))

    length: int = len(melody)
    i: int = 0
    pause: int = 0
    while i < length:
        if melody[i] == 0:
            pause += 1
            i += 1
            while i < length and melody[i] == NOTES + 1:
                pause += 1
                i += 1
        elif 1 <= melody[i] <= NOTES:
            note: int = melody[i] + 52
            duration: int = 1
            i += 1
            while i < length and melody[i] == NOTES + 1:
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
        Volume of music, ranging from 0.0 to 1.0
    """
    pygame.mixer.init()
    clock = pygame.time.Clock()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(volume)
    while pygame.mixer.music.get_busy():
        clock.tick(30)
