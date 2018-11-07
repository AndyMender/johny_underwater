"""
    Entity classes implementing movement

    author: Andy Mender <andymenderunix@gmail.com>
    date: 2018-11-04
"""

import logging
import random

from libs.constants import ANIM_GROUPS, ANIM_RESET
from libs.entity.base import Entity
from libs.entity.animated import MovingAnimEntity
from libs.utilities import timestamp_now

# set up logging
logger = logging.getLogger(__file__)


# TODO: add collision detection to movement methods
class MovingEntity(Entity):
    """Entity child class with movement implementation."""

    def __init__(self, sprite_group: str, speed: int = 1):
        super().__init__(sprite_group)

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
        self.clock = timestamp_now()    # reset clock after movement

    def move_down(self) -> None:
        self.rect.y += self.speed
        self.state = "down"
        self.clock = timestamp_now()    # reset clock after movement

    def move_left(self) -> None:
        self.rect.x -= self.speed
        self.state = "left"
        self.clock = timestamp_now()    # reset clock after movement

    def move_right(self) -> None:
        self.rect.x += self.speed
        self.state = "right"
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

        # run parent class base update procedure
        super().update()


class RandomMovingEntity(MovingAnimEntity):
    """Base class for randomly moving creatures."""

    def move_random(self) -> None:
        """Move entity in a random direction."""

        # get state at random
        state = random.choice(ANIM_GROUPS)

        # execute motion or switch to "idle"
        if state in self.movements:
            self.movements[state]()

        elif state == "idle":
            self.state = "idle"

    def update(self) -> None:
        """Update AI entity state."""

        # move in random direction
        self.move_random()

        # run parent class base update procedure
        super().update()


class ProjectileEntity(MovingEntity):
    """Base class for unidirectionally moving projectiles
    (bolts, arrows, fireballs, etc.)"""

    def __init__(self, sprite_group: str, direction: str, speed: int = 1):

        # set vector direction via internal state
        self.state = direction

        # set speed and sprite group / name via parent
        super().__init__(sprite_group, speed)

    def shoot(self) -> None:
        """Move projectile in selected direction."""

        self.movements[self.state]()

    def update(self):
        """Update entity state."""

        # move in selected direction
        self.shoot()

        # check "alive" status
        # NOTE: parent class update() could revert state to "idle"
        # which is to be avoided!
        self.is_alive()
