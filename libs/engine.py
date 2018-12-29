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
from libs.entity.player import player_obj

# set up logging
logger = logging.getLogger(__file__)


class Engine:
    """Main handler class for controlling the pygame engine."""

    def __init__(self):
        # set up main pygame params
        self.screen = None
        self.screen_rect = None
        self.fonts = None
        self.music = None
        self.gfx = None
        self.sfx = None
        self.clock = None
        self.map = None
        self.collision_map = None          # TODO: populate with collision coordinates
        self.entities = None

        # link pygame and set flags
        self.screen_flags = pygame.HWSURFACE | pygame.DOUBLEBUF

    def init(self) -> None:
        """Main pygame init function."""

        # start pygame and set up display
        pygame.init()
        pygame.display.set_caption(TITLE_BAR)

        # set up key handling
        pygame.key.set_repeat(1, 3)

        # set up screen and render flags
        self.screen = pygame.display.set_mode(SCREEN_SIZE, self.screen_flags)
        self.screen_rect = self.screen.get_rect()

        # set up controllers
        pygame.mouse.set_visible(False)

        # set up music mixer
        self.music = pygame.mixer.music

        # prepare entity container for tracking
        self.entities = pygame.sprite.Group()

        # start the game clock
        self.clock = pygame.time.Clock()

    def main_loop(self) -> int:
        """Main game loop.

        :return: error code depending on exit condition
        """

        while True:
            # capture key/mouse events and respond
            for event in pygame.event.get():
                # main window events
                if event.type == pygame.QUIT:
                    pygame.quit()

                    return PYGAME_SUCCESS

                # key-press events
                elif event.type == pygame.KEYDOWN:
                    # TODO: split player and menu events
                    player_obj.handle_event(event)

            # TODO: insert main game events HERE!

            # redraw map to remove dead objects
            self.refresh_map()

            # update entity state and redraw
            self.entities.update()
            self.entities.draw(self.screen)

            # refresh main display surface
            pygame.display.update()

            # limit screen refresh rate
            self.clock.tick(FPS)

    def refresh_map(self) -> None:
        """Reload currently loaded map."""

        if self.map is not None:
            # NOTE: below code was adapted from:
            # https://www.reddit.com/r/pygame/comments/2oxixc/pytmx_tiled/

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

                        # TODO: load entities from map objects

                        # objects with points are polygons or lines
                        if hasattr(obj, "points") and obj.points is not None:
                            pygame.draw.lines(self.screen, LINE_COLOR,
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

                            # draw objects on alpha surface
                            pygame.draw.rect(alpha_screen, COLLISION_COLOR,
                                             obj_dims, 3)

                            # blit alpha surface to display surface (applies transparency)
                            self.screen.blit(alpha_screen, (0, 0))

                # draw image layers
                elif isinstance(layer, pytmx.TiledImageLayer):
                    if hasattr(layer, "image") and layer.image is not None:
                        self.screen.blit(layer.image, (0, 0))

    def load_map(self, map_file: str) -> bool:
        """Load and render a Tiled game map.

        :param map_file: path to Tiled TMX map file
        :return: True on successful map load, False on failure
        """

        # validate map file extension and path
        if not map_file.endswith(".tmx"):
            logger.warning(f"Wrong file extension for map file: {map_file}")
            return False

        if not os.path.exists(map_file):
            logger.warning(f"Path to map file does not exist: {map_file}")
            return False

        # extract data from mapfile and link to Engine
        self.map = load_pygame(map_file)

        # send map sprites and objects to display surface
        self.refresh_map()

        return True


# instantiate engine for use by other modules
game_engine = Engine()
