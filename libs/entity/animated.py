"""
    Entity classes implementing animations

    author: Andy Mender <andymenderunix@gmail.com>
    date: 2018-11-04
"""

import logging
import os.path
import re

import pygame

from libs.constants import SPRITE_DIR
from libs.entity.base import Entity

# set up logging
logger = logging.getLogger(__file__)


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