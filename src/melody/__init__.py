import os, sys

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from .midi import save_midi, play_midi
from .music import Melody, Note, Tonality
