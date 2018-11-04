"""
    Classes representing in-game entities (characters, monsters and projectiles)

    author: Andy Mender <andymenderunix@gmail.com>
    date: 2018-11-03
"""

import logging
import os
import os.path
import re
from typing import Union

import pygame

# set up logging
logger = logging.getLogger(__file__)


class Entity(pygame.sprite.Sprite):
    """Base class for in-game entities."""

    def __init__(self, sprite_file: str):

        # set up base sprite properties from parent class
        super().__init__()

        # validate sprite
        if not sprite_file.endswith(".png"):
            raise ValueError("Only PNG sprites are allowed"
                             " due to higher image quality.")

        if not os.path.exists(sprite_file):
            raise RuntimeError(f"Sprite path does not exist: {sprite_file}")

        # placeholders for sprite objects
        self.image = None
        self.rect = None

        # load sprite image and build sprite rect
        # NOTE: used to redraw sprites to display surface by pygame.sprite.Group.draw()
        self.load_sprite(sprite_file)

        # set up base entity attributes
        self.hp: Union[float, int] = 1

    def load_sprite(self, sprite_obj: Union[str, pygame.Surface]) -> None:
        """Load sprite from file or from pre-loaded Surface."""

        if type(sprite_obj) == str:
            self.image = pygame.image.load(sprite_obj)

        elif type(sprite_obj) == pygame.Surface:
            self.image = sprite_obj

        # apply current 'x' and 'y' coordinates to new sprite rect
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
        """Generic update method - to be used later or in child classes."""

        # check "alive" status
        self.is_alive()


# TODO: add collision detection to movement methods
class MovingEntity(Entity):
    """Entity child class with movement implementation."""

    def __init__(self, sprite_file: str, speed: int = 1):
        super().__init__(sprite_file)

        # multiplier for pixel displacement
        self.speed: int = speed

        # tracker for anim group selection based on direction
        self.direction: str = None

    def move_up(self) -> None:
        self.rect.y -= self.speed
        self.direction = "up"

    def move_down(self) -> None:
        self.rect.y += self.speed
        self.direction = "down"

    def move_left(self) -> None:
        self.rect.x -= self.speed
        self.direction = "left"

    def move_right(self) -> None:
        self.rect.x += self.speed
        self.direction = "right"


class AnimEntity(Entity):
    """Entity child class with animation frames."""

    def __init__(self, sprite_file: str):
        super().__init__(sprite_file)

        # placeholders for animation properties
        self.anim_frames: list = []
        self.frame_num: int = 0
        self.counter: int = 0

        # collect animation frames and set frame number
        # TODO: allow more than 10 frames?
        anim_format = re.compile("_[0-9]\.png$")

        if anim_format.search(sprite_file):
            anim_dir = os.path.dirname(sprite_file)

            for anim_file in sorted(os.listdir(anim_dir)):
                if anim_format.search(anim_file):
                    anim_path = os.path.join(anim_dir, anim_file)

                    self.anim_frames.append(pygame.image.load(anim_path))

            # count frames for cycling
            self.frame_num = len(self.anim_frames)

    def animate(self):
        """Load next animation frame."""

        # increment counter and pick animation frame
        self.counter += 1

        curr_anim = self.counter % self.frame_num

        self.load_sprite(self.anim_frames[curr_anim])

        # reset counter if it hits last frame
        if curr_anim == 0:
            self.counter = 0

    def update(self):
        """Update animated sprite state."""

        # trigger animation
        self.animate()

        # run parent class base update procedure
        super().update()