"""
    Player entity class and related functions

    author: Andy Mender <andymenderunix@gmail.com>
    date: 2018-11-04
"""

import pygame

from libs.constants import MOVEMENT_KEYS
from libs.entity.animated import MovingAnimEntity


class PlayerEntity(MovingAnimEntity):
    """Player entity class."""

    def handle_event(self, event: pygame.event.EventType) -> None:
        """Main player0 event handler."""

        self.movement_events = {
            pygame.K_UP: self.move_up,
            pygame.K_DOWN: self.move_down,
            pygame.K_LEFT: self.move_left,
            pygame.K_RIGHT: self.move_right,
        }

        # handle movement keys
        if event.key in MOVEMENT_KEYS:
            self.movement_events[event.key]()


player_obj = PlayerEntity("player0", 10)