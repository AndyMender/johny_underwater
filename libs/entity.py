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
import time

import pygame

from libs.constants import SPRITE_DIR, ANIM_GROUPS, ANIM_RESET

# set up logging
logger = logging.getLogger(__file__)


class Entity(pygame.sprite.Sprite):
    """Base class for in-game entities."""

    state: str = "idle"          # changed in classes implementing movement
    name: str = None             # entity name or sprite group

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
        sprite_path = os.path.join(sprites, os.listdir(sprites)[0])

        # validate sprite
        if not sprite_path.endswith(".png"):
            raise ValueError("Only PNG sprites are allowed"
                             " due to higher image quality.")

        if not os.path.exists(sprite_path):
            raise RuntimeError(f"Sprite path does not exist: {sprite_path}")

        # placeholders for sprite objects
        self.image = None
        self.rect = None

        # load sprite image and build sprite rect
        # NOTE: used to redraw sprites to display surface by pygame.sprite.Group.draw()
        self.load_sprite(sprite_path)

        # set up base entity attributes
        self.hp: Union[float, int] = 1

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


# TODO: add collision detection to movement methods
class MovingEntity(Entity):
    """Entity child class with movement implementation."""

    def __init__(self, sprite_group: str, speed: int = 1):
        super().__init__(sprite_group)

        # multiplier for pixel displacement
        self.speed: int = speed

        # internal clock for state reset
        self.clock = round(time.time())

    def move_up(self) -> None:
        self.rect.y -= self.speed
        self.state = "up"

    def move_down(self) -> None:
        self.rect.y += self.speed
        self.state = "down"

    def move_left(self) -> None:
        self.rect.x -= self.speed
        self.state = "left"

    def move_right(self) -> None:
        self.rect.x += self.speed
        self.state = "right"

    def reset_state(self) -> None:
        """Check if state needs to be reset to "idle" due to inactivity."""

        timer = round(time.time())

        if (timer - self.clock) >= ANIM_RESET:
            self.state = "idle"
            self.clock = timer

    def update(self) -> None:
        """Update moving sprite state."""

        # check state and reset if needed
        self.reset_state()

        # run parent class base update procedure
        super().update()


class AnimEntity(Entity):
    """Entity child class with animation frames."""

    def __init__(self, sprite_group: str):
        # load starting animation via parent class
        super().__init__(sprite_group)

        # animation properties
        self.anim_frames: list = []
        self.frame_num: int = 0
        self.counter: int = 0
        self.anim_groups: dict = {self.state: []}

        # collect animation frames and set frame number
        self.load_animations()

    def load_animations(self) -> None:
        """Load all animation frames into attribute dict."""

        # only collect valid frame images
        # TODO: allow more than 10 frames?
        anim_format = re.compile("_[0-9]\.png$")

        # collection for frame numbers for all animation groups
        frame_numbers = []

        for anim_group in self.anim_groups:
            anim_dir = os.path.join(SPRITE_DIR, self.name, anim_group)

            for anim_file in sorted(os.listdir(anim_dir)):
                if anim_format.search(anim_file):
                    anim_path = os.path.join(anim_dir, anim_file)

                    self.anim_groups[anim_group].append(pygame.image.load(anim_path))

            frame_numbers.append(len(self.anim_groups[anim_group]))

        # count until the shortest animation's last frame
        self.frame_num = min(frame_numbers)

    def animate(self) -> None:
        """Load next animation frame."""

        # cycle only when multiple frames are present
        if self.frame_num > 1:
            # increment counter and pick animation frame
            self.counter += 1

            curr_anim = self.counter % self.frame_num

            self.load_sprite(self.anim_groups[self.state][curr_anim])

            # reset counter if it hits last frame
            if curr_anim == 0:
                self.counter = 0

    def update(self) -> None:
        """Update animated sprite state."""

        # trigger animation
        self.animate()

        # run parent class base update procedure
        super().update()