"""Game Template."""

# from gameobject import GameObject
import pygame

from constants import *


class GameTemplate(object):
    """pygame object."""

    def __init__(self):
        """Constructor."""
        pygame.display.init()
        pygame.display.set_mode((1080, 720))
        self.deltatime = 0.0

    def startup(self):
        """Do startup routines."""
        return True

    def update(self):
        """Input and time."""
        return True

    def draw(self):
        pygame.display.flip()
        return True

    def shutdown(self):
        """Shutdown Game properly."""
        return True
