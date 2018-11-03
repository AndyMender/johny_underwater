"""
    Game engine classes, functions and attributes

    author: Andy Mender <andymenderunix@gmail.com>
    date: 2018-11-03
"""

import pygame

from libs.constants import SCREEN_SIZE, TITLE_BAR


class Engine:
    """Main handler class for controlling the pygame engine"""

    def __init__(self):
        # set up main pygame params
        self.SCREEN = None
        self.SCREEN_RECT = None
        self.FONTS = None
        self.MUSIC = None
        self.GFX = None

        # link pygame and set flags
        self.pg = pygame
        self.pg_flags = self.pg.HWSURFACE | self.pg.DOUBLEBUF

    def init_pygame(self) -> None:
        """Main pygame init function

        :return:
        """

        # start pygame, set up screen and rendering flags
        self.pg.init()
        self.pg.display.set_caption(TITLE_BAR)

        self.SCREEN = self.pg.display.set_mode(SCREEN_SIZE, self.pg_flags)

        self.SCREEN_RECT = self.SCREEN.get_rect()

        self.pg.mouse.set_visible(False)

    def main_loop(self) -> bool:
        """Main game loop

        :return: True on correct exit, False on failure
        """

        while True:
            for event in self.pg.event.get():
                if event.type == self.pg.QUIT:
                    return True
