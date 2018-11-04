"""
    Character and monster entity classes and related functions

    author: Andy Mender <andymenderunix@gmail.com>
    date: 2018-11-04
"""

import random

from libs.constants import ANIM_GROUPS
from libs.entity import MovingEntity


class RandomAIEntity(MovingEntity):
    """Base class for randomly moving creatures."""

    def move_random(self) -> None:
        """Move entity in a random direction."""

        # movement mapper
        movements = {"up": self.move_up,
                     "down": self.move_down,
                     "left": self.move_left,
                     "right": self.move_right}

        # get state at random
        state = random.choice(ANIM_GROUPS)

        # execute motion
        if state in movements:
            movements[state]()

        elif state == "idle":
            self.state = "idle"

    def update(self) -> None:
        """Update AI entity state."""

        # move in random direction
        self.move_random()

        # run parent class base update procedure
        super().update()