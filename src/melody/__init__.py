import os, sys

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from .midi import save_midi, play_midi, read_midi
from .music import Melody, Note, Tonality
from .music import Note, Melody, Tonality, TONALITY, STABILITY, get_stability, get_tonality
