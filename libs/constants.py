"""
    Constants and static parameters used by the game

    author: Andy Mender <andymenderunix@gmail.com>
    date: 2018-11-02
"""

import os.path
import pathlib

import pygame

# TODO: consider grouping constants into enum-like classes
# path constants
BASEDIR: str = os.path.join(*pathlib.Path(os.path.realpath(__file__)).parts[:-2])
ASSETS_DIR: str = os.path.join(BASEDIR, "assets")
MAP_DIR: str = os.path.join(ASSETS_DIR, "maps")
TILE_DIR: str = os.path.join(ASSETS_DIR, "tiles")
SPRITE_DIR: str = os.path.join(ASSETS_DIR, "sprites")
SFX_DIR: str = os.path.join(ASSETS_DIR, "sfx")
MUSIC_DIR: str = os.path.join(ASSETS_DIR, "music")
OBJ_DIR: str = os.path.join(ASSETS_DIR, "objects")

# exit status codes
PYGAME_FAILED: int = -1
PYGAME_SUCCESS: int = 0
PYGAME_ERROR: int = 1

# pygame constants
SCREEN_SIZE: tuple = (640, 480)
TITLE_BAR: str = "Johny Underwater"
FPS: int = 8
COLLISION_COLOR: tuple = (255, 0, 0, 100)
LINE_COLOR: tuple = (0, 255, 0)
ANIM_RESET: int = 30

# event and key constants
PLAYER_EVENTS = (pygame.KEYDOWN,)
MOVEMENT_KEYS = (pygame.K_UP, pygame.K_DOWN,
                 pygame.K_LEFT, pygame.K_RIGHT)

# animation constants
ANIM_GROUPS = ("idle", "up", "down", "left", "right")
