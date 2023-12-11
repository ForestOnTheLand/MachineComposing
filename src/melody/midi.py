import pygame
from mido import Message, MidiFile, MidiTrack
from typing import List
from .music import Note, Melody


def save_midi(
    melody: Melody,
    path: str,
    *,
    instrument: int = 0,
    velocity: int = 64,
    time: int = 240,
) -> None:
    """
    Save a melody into a midi file. For more information about midi files, see
    https://www.midi.org/specifications.
    
    Parameters
    ----------
    `melody` : `Melody`
        The melody
    `path` : `str`
        Path of output file
    `instrument` : `int`, optional
        Instrument type, from 0 to 127. 
        See https://blog.csdn.net/ruyulin/article/details/84103186 for more details.
        By default `0`.
    `velocity` : `int`, optional
        Volume of voice, from 0 ro 127.
        By default `64`.
    `time` : `int`, optional
        Time of a eighth note.
        By default `240`
    
    Raises
    ------
    `ValueError`
        if melody is not convertable to Melody.
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
        if melody[i].id == 0:
            pause += 1
            i += 1
            while i < length and melody[i].id == Note.NUM + 1:
                pause += 1
                i += 1
        elif 1 <= melody[i].id <= Note.NUM:
            note: int = melody[i].id + 52
            duration: int = 1
            i += 1
            while i < length and melody[i].id == Note.NUM + 1:
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
