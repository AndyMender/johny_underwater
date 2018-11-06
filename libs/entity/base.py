"""
    Base entity class

    author: Andy Mender <andymenderunix@gmail.com>
    date: 2018-11-04
"""

import logging
import os
import os.path
from typing import Union

import pygame

from libs.constants import SPRITE_DIR

# set up logging
logger = logging.getLogger(__file__)


class Entity(pygame.sprite.Sprite):
    """Base class for in-game entities."""

    state: str = "idle"          # changed in classes implementing movement
    name: str = None             # entity name or sprite group

    # placeholders for sprite objects
    image = None
    rect = None

    # base entity attributes
    hp: Union[float, int] = 1

    def __init__(self, sprite_group: str):

        # set up base sprite properties from parent class
        super().__init__()

        # assign name from sprite group (IMPORTANT!)
        self.name = sprite_group

        # get dir for sprite group and validate
        sprites = os.path.join(SPRITE_DIR, sprite_group, self.state)

        if not os.path.exists(sprites):
            raise ValueError(f"Path to sprite group dir missing: {sprites}")

        # get path to first sprite
        sprite_path = os.path.join(sprites, sorted(os.listdir(sprites))[0])

        # validate sprite
        if not sprite_path.endswith(".png"):
            raise ValueError("Only PNG sprites are allowed"
                             " due to higher image quality.")

        if not os.path.exists(sprite_path):
            raise RuntimeError(f"Sprite path does not exist: {sprite_path}")

        # load sprite image and build sprite rect
        # NOTE: used to redraw sprites to display surface by pygame.sprite.Group.draw()
        self.load_sprite(sprite_path)

    def load_sprite(self, sprite_obj: Union[str, pygame.Surface]) -> None:
        """Load sprite from file or from pre-loaded Surface."""

        if type(sprite_obj) == str:
            self.image = pygame.image.load(sprite_obj)

        elif type(sprite_obj) == pygame.Surface:
            self.image = sprite_obj

        # apply current 'x' and 'y' coordinates to new sprite rect
        # NOTE: prevents coordinate reset
        if self.rect is not None:
            x, y = self.rect.x, self.rect.y
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = x, y
        else:
            self.rect = self.image.get_rect()

    def is_alive(self) -> None:
        """Check for entity "alive" status."""

        if self.hp <= 0:
            self.kill()

    def update(self) -> None:
        """Base update method - overridden in child classes."""

        # check "alive" status
        self.is_alive()
