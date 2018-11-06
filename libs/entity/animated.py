"""
    Entity classes implementing animations

    author: Andy Mender <andymenderunix@gmail.com>
    date: 2018-11-04
"""

import logging
import os.path
import re

import pygame

from libs.constants import ANIM_GROUPS, ANIM_RESET, SPRITE_DIR
from libs.entity.base import Entity
from libs.utilities import timestamp_now

# set up logging
logger = logging.getLogger(__file__)


class AnimEntity(Entity):
    """Entity child class with animation frames."""

    # animation properties
    frame_num: int = 0
    counter: int = 0

    def __init__(self, sprite_group: str):
        # load initial animation frame via parent class
        super().__init__(sprite_group)

        # collection for animations per state
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

        # make sure name was set properly
        if self.name is None:
            raise ValueError("Attribute 'name' not set!")

        for anim_group in self.anim_groups:
            anim_dir = os.path.join(SPRITE_DIR, self.name, anim_group)

            # fail if directory defining state is missing
            if not os.path.isdir(anim_dir):
                raise FileNotFoundError(f"Anim group directory missing: {anim_dir}")

            anim_listing = sorted(os.listdir(anim_dir))

            if len(anim_listing) == 0:
                raise FileNotFoundError("At least 1 animation frame per state is required!")

            for anim_file in anim_listing:
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


class MovingAnimEntity(AnimEntity):
    """Base class for objects implementing animations dependent on movement."""

    def __init__(self, sprite_group: str, speed: int = 1):
        # load initial animation frame and "idle" anims via parent class
        super().__init__(sprite_group)

        # collection for animations per state
        self.anim_groups: dict = {state: [] for state in ANIM_GROUPS}

        # reload animations for all states
        self.load_animations()

        # multiplier for pixel displacement
        self.speed: int = speed

        # internal clock for state reset
        self.clock = timestamp_now()

        # movement mapper
        self.movements = {"up": self.move_up,
                          "down": self.move_down,
                          "left": self.move_left,
                          "right": self.move_right}

    def move_up(self) -> None:
        self.rect.y -= self.speed
        self.state = "up"
        self.animate()                  # jump to next anim frame
        self.clock = timestamp_now()    # reset clock after movement

    def move_down(self) -> None:
        self.rect.y += self.speed
        self.state = "down"
        self.animate()                  # jump to next anim frame
        self.clock = timestamp_now()    # reset clock after movement

    def move_left(self) -> None:
        self.rect.x -= self.speed
        self.state = "left"
        self.animate()                  # jump to next anim frame
        self.clock = timestamp_now()    # reset clock after movement

    def move_right(self) -> None:
        self.rect.x += self.speed
        self.state = "right"
        self.animate()                  # jump to next anim frame
        self.clock = timestamp_now()    # reset clock after movement

    def reset_state(self) -> None:
        """Check if state needs to be reset to "idle" due to inactivity."""

        current_time = timestamp_now()

        if (current_time - self.clock) >= ANIM_RESET:
            self.state = "idle"
            self.clock = current_time

    def update(self) -> None:
        """Update moving sprite state."""

        # check state and reset if needed
        self.reset_state()

        # parent update() skipped to trigger animations only on movement
        self.is_alive()
