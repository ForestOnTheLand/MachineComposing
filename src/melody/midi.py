import pygame
from mido import Message, MetaMessage, MidiFile, MidiTrack
from typing import List
from .music import Note, Melody, get_tonality


def save_midi(
    melody: Melody,
    path: str,
    *,
    instrument: int = 0,
    velocity: int = 64,
    time: int = 240,
    tonality: str | None = None,
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
    `tonality`:
        valid values: A A#m Ab Abm Am B Bb Bbm Bm C C# C#m Cb Cm D D#m Db Dm E Eb Ebm Em F F# F#m Fm G G#m Gb Gm

    Raises
    ------
    `ValueError`
        if melody is not convertable to Melody.
    """
    if not isinstance(melody, Melody):
        melody = Melody(melody)

    mid = MidiFile()
    track = MidiTrack()
    mid.ticks_per_beat = 2 * time
    mid.tracks.append(track)

    track.append(Message('program_change', program=instrument))
    track.append(MetaMessage('time_signature', numerator=4, denominator=4))
    if tonality is not None:
        track.append(MetaMessage('key_signature', key=tonality))

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

    track.append(MetaMessage('end_of_track', time=time * pause))
    mid.save(path)


def read_midi(path: str) -> Melody:
    """parse a midi file into Melody.
    """
    file = MidiFile(path, type=0)
    track = file.tracks[0]
    eight_note = file.ticks_per_beat / 2
    note_list = []
    for message in track:
        if not message.is_meta:
            print(message)
            assert message.time % eight_note == 0, "Durations must be multiples of eigth_note"
            duration = int(message.time / eight_note)
            if message.type == 'note_on':
                assert 53 <= message.note <= Note.NUM + 52, "Note must be in [F3, G5]"
                if duration:
                    note_list += [0] + [Note.NUM + 1] * (duration - 1)
                note_list += [message.note - 52]
            elif message.type == 'note_off':
                assert 53 <= message.note <= Note.NUM + 52, "Note must be in [F3, G5]"
                if duration:
                    note_list += [Note.NUM + 1] * (duration - 1)
                else:
                    note_list.pop()
        else:
            if message.type == 'end_of_track':
                assert message.time % eight_note == 0, "Durations must be multiples of eigth_note"
                duration = int(message.time / eight_note)
                if duration:
                    note_list += [0] + [Note.NUM + 1] * (duration - 1)
                break

    return Melody(note_list)


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
