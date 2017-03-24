"""Concrete game."""
import boids
from game import GameTemplate
import pygame

class ConcreteGame(GameTemplate):
    """Need documentation."""

    def __init__(self, name):
        """Need documentation."""
        super(ConcreteGame, self).__init__()
        self._name = name
        self._gameobjects = []
        self.targetboid = boids.Agent()

    def addtobatch(self, gameobject):
        """Add gameobjects to this game."""
        self._gameobjects.append(gameobject)

    def update(self):
        """Update this games logic."""
        if not super(ConcreteGame, self).update():
            return False
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
        self.targetboid.position = pygame.mouse.get_pos()
        for gameobjs in self._gameobjects:
            gameobjs.update(self.deltatime)
        return True

    def draw(self):
        '''draw all gameobjects added to this game'''
        for gameobj in self._gameobjects:
            gameobj.draw()
        super(ConcreteGame, self).draw()

    def run(self):
        '''need documentation'''
        if super(ConcreteGame, self).startup():
            while self.update():
                self.draw()
        super(ConcreteGame, self).shutdown()
