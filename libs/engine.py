"""
    Game engine classes, functions and attributes

    author: Andy Mender <andymenderunix@gmail.com>
    date: 2018-11-03
"""

import logging
import os.path

import pygame
import pytmx
from pytmx.util_pygame import load_pygame

from libs.constants import (COLLISION_COLOR, FPS, LINE_COLOR, PYGAME_ERROR,
                            PYGAME_FAILED, PYGAME_SUCCESS, SCREEN_SIZE,
                            TITLE_BAR)

# set up logging
logger = logging.getLogger(__file__)


class Engine:
    """Main handler class for controlling the pygame engine"""

    def __init__(self):
        # set up main pygame params
        self.screen = None
        self.screen_rect = None
        self.fonts = None
        self.music = None
        self.gfx = None
        self.sfx = None

        self.map = None

        # link pygame and set flags
        self.pg = pygame
        self.screen_flags = self.pg.HWSURFACE | self.pg.DOUBLEBUF

        # start the game clock
        self.clock = self.pg.time.Clock()

    def init(self) -> None:
        """Main pygame init function

        :return:
        """

        # start pygame, set up screen and rendering flags
        self.pg.init()
        self.pg.display.set_caption(TITLE_BAR)

        self.screen = self.pg.display.set_mode(SCREEN_SIZE, self.screen_flags)
        self.screen_rect = self.screen.get_rect()

        # set up controllers
        self.pg.mouse.set_visible(False)

    def main_loop(self) -> bool:
        """Main game loop

        :return: True on correct exit, False on failure
        """

        while True:
            # TODO: insert main game events HERE!

            # capture key/mouse events and respond
            for event in self.pg.event.get():
                if event.type == self.pg.QUIT:
                    self.pg.quit()

                    return PYGAME_SUCCESS

            self.pg.display.update()

            # limit screen refresh rate
            self.clock.tick(FPS)

    def load_map(self, mapfile: str) -> bool:
        """Load and render a Tiled game map

        :param mapfile: path to Tiled map file
        :return: True on successful map load, False on failure
        """

        # validate map file extension and path
        if not mapfile.endswith(".tmx"):
            logger.warning(f"Wrong file extension for map file: {mapfile}")
            return False

        elif not os.path.exists(mapfile):
            logger.warning(f"Path to map file does not exist: {mapfile}")
            return False

        # extract data from mapfile and link to Engine
        self.map = load_pygame(mapfile)

        # NOTE: below code was adapted from:
        # https://www.reddit.com/r/pygame/comments/2oxixc/pytmx_tiled/

        # set background color if applicable
        if self.map.background_color:
            self.screen.fill(self.pg.Color(self.map.background_color))

        # loop over layers and draw according to type
        for layer in self.map.visible_layers:

            # draw regular map tiles
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, image in layer.tiles():
                    image_dims = (x * self.map.tilewidth,
                                  y * self.map.tileheight)

                    self.screen.blit(image, image_dims)

            # draw objects
            elif isinstance(layer, pytmx.TiledObjectGroup):

                for obj in layer:

                    # objects with points are polygons or lines
                    if hasattr(obj, "points") and obj.points is not None:
                        self.pg.draw.lines(self.screen, LINE_COLOR,
                                           obj.closed, obj.points, 3)

                    # some objects contain images - blit them
                    elif hasattr(obj, "image") and obj.image is not None:
                        obj_dims = (obj.x, obj.y)

                        self.screen.blit(obj.image, obj_dims)

                    # draw a rect for other objects (collision zones, events, etc.)
                    # TODO: separate event objects from collision markers
                    else:
                        obj_dims = (obj.x, obj.y, obj.width, obj.height)

                        # create alpha-capable surface
                        alpha_screen = self.screen.convert_alpha()

                        self.pg.draw.rect(alpha_screen, COLLISION_COLOR,
                                          obj_dims, 3)

                        # blit alpha layer to display surface (applies transparency)
                        self.screen.blit(alpha_screen, (0, 0))

            # draw image layers
            elif isinstance(layer, pytmx.TiledImageLayer):
                if hasattr(layer, "image") and layer.image is not None:
                    self.screen.blit(layer.image, (0, 0))

        return True

game_engine = Engine()