import logging
import os.path
import sys

from libs.constants import (MAP_DIR, PYGAME_ERROR, PYGAME_FAILED,
                            PYGAME_SUCCESS, SPRITE_DIR)
from libs.engine import game_engine
from libs.entity import AnimEntity
from libs.npc import RandomAIEntity

# set up main logger
logger = logging.getLogger(__file__)

if __name__ == '__main__':

    # start game engine and load elements
    game_engine.init()

    game_engine.load_map(os.path.join(MAP_DIR, "project1.tmx"))

    # create motionless animated bubbles
    bubbles1 = AnimEntity("bubbles0")
    bubbles1.rect.x = 20
    bubbles1.rect.y = 20

    # create randomly moving static bubbles
    bubbles2 = RandomAIEntity("bubbles0")
    bubbles2.rect.x = 100
    bubbles2.rect.y = 100
    bubbles2.speed = 10

    # add objects to group
    game_engine.entities.add(bubbles1)
    game_engine.entities.add(bubbles2)

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
