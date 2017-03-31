"""Game Template."""

# from gameobject import GameObject
import pygame


class GameTemplate(object):
    """pygame object."""

    def __init__(self):
        """Constructor."""
        pygame.display.init()
        self.surface = pygame.display.set_mode((1080, 720))
        self.clock = pygame.time.Clock()
        self.background = pygame.Surface(self.surface.get_size()).convert()
        self.background.fill((0, 0, 0))
        self.deltatime = 0.0

    def startup(self):
        """Do startup routines."""
        return True

    def update(self):
        """Input and time."""
        return True

    def draw(self):
        """Draw function for general game."""
        pygame.display.flip()
        self.surface.blit(self.background, (0, 0))
        return True

    def shutdown(self):
        """Shutdown Game properly."""
        return True
