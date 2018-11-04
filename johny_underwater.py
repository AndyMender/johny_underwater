import logging
import os.path
import sys

from libs.constants import (MAP_DIR, PYGAME_ERROR, PYGAME_FAILED,
                            PYGAME_SUCCESS, SPRITE_DIR)
from libs.engine import game_engine
from libs.entity import AnimEntity

# set up main logger
logger = logging.getLogger(__file__)

if __name__ == '__main__':

    # start game engine and load elements
    game_engine.init()

    game_engine.load_map(os.path.join(MAP_DIR, "project1.tmx"))

    # add animated object to map
    bubbles = AnimEntity("bubbles0")
    bubbles.rect.x = 20
    bubbles.rect.y = 20

    game_engine.entities.add(bubbles)

    # get status code while exiting main loop
    exit_status = game_engine.main_loop()

    if exit_status == PYGAME_SUCCESS:
        logger.debug("Pygame engine exited successfully.")
        sys.exit(PYGAME_SUCCESS)

    elif exit_status == PYGAME_ERROR:
        logger.warning("Pygame engine encountered an error.")
        sys.exit(PYGAME_ERROR)

    elif exit_status == PYGAME_FAILED:
        logger.critical("Pygame engine encoutered a critical error"
                        " and had to be terminated.")
        sys.exit(PYGAME_FAILED)
