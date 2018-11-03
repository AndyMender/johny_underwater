"""
    Constants and static parameters used by the game

    author: Andy Mender <andymenderunix@gmail.com>
    date: 2018-11-02
"""

import os.path
import pathlib

# pygame constants
SCREEN_SIZE = (600, 400)
TITLE_BAR = 'Johny Underwater'

# path constants
BASEDIR = os.path.join(*pathlib.Path(os.path.realpath(__file__)).parts[:-2])
ASSETS_DIR = os.path.join(BASEDIR, "assets")
MAP_DIR = os.path.join(ASSETS_DIR, "maps")
SPRITE_DIR = os.path.join(ASSETS_DIR, "sprites")
SFX_DIR = os.path.join(ASSETS_DIR, "sfx")
MUSIC_DIR = os.path.join(ASSETS_DIR, "music")
