"""
    Constants and static parameters used by the game

    author: Andy Mender <andymenderunix@gmail.com>
    date: 2018-11-02
"""

import os.path
import pathlib

import pygame

# TODO: consider grouping constants into enum-like classes

# pygame constants
SCREEN_SIZE = (640, 480)
TITLE_BAR = 'Johny Underwater'
FPS = 10
COLLISION_COLOR = (255, 0, 0, 100)
LINE_COLOR = (0, 255, 0)

# event and key constants
PLAYER_EVENTS = (pygame.KEYDOWN,)
MOVEMENT_KEYS = (pygame.K_UP, pygame.K_DOWN,
                 pygame.K_LEFT, pygame.K_RIGHT)

# path constants
BASEDIR = os.path.join(*pathlib.Path(os.path.realpath(__file__)).parts[:-2])
ASSETS_DIR = os.path.join(BASEDIR, "assets")
MAP_DIR = os.path.join(ASSETS_DIR, "maps")
SPRITE_DIR = os.path.join(ASSETS_DIR, "sprites")
SFX_DIR = os.path.join(ASSETS_DIR, "sfx")
MUSIC_DIR = os.path.join(ASSETS_DIR, "music")
OBJ_DIR = os.path.join(ASSETS_DIR, "objects")

# exit status codes
PYGAME_FAILED = -1
PYGAME_SUCCESS = 0
PYGAME_ERROR = 1
