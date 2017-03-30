"""Concrete game."""
import math

import pygame
import random
import boids
from game import GameTemplate


class ConcreteGame(GameTemplate):
    """Need documentation."""

    # pylint: disable=no-member

    def __init__(self, name):
        """Need documentation."""
        super(ConcreteGame, self).__init__()
        self._name = name
        self.flee = False
        self.wander = True
        pygame.font.init()
        self.font = pygame.font.SysFont('mono', 20)
        self._gameobjects = []
        self.targetboid = boids.Agent((pygame.display.get_surface(
        ).get_width(), pygame.display.get_surface().get_height()))

    def addtobatch(self, gameobject):
        """Add gameobjects to this game."""
        self._gameobjects.append(gameobject)
        if type(gameobject) == boids.Agent:
            gameobject.settarget(self.targetboid)

    def update(self):
        """Update this games logic."""
        self.clock.tick(60)
        self.deltatime = float(self.clock.get_time()) / float(1000)
        if not super(ConcreteGame, self).update():
            return False
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_f:
                    self.flee = True
                    self.wander = False
                if event.key == pygame.K_s:
                    self.flee = False
                    self.wander = False
                if event.key == pygame.K_w:
                    self.wander = True
                    self.flee = False
                if event.key == pygame.K_SPACE:
                    self.addtobatch(boids.Agent((pygame.display.get_surface(
                    ).get_width(),
                        pygame.display.get_surface().get_height())))
                if event.key == pygame.K_DELETE:
                    if len(self._gameobjects) > 0:
                        self._gameobjects.remove(
                            self._gameobjects[
                                random.randrange(0, len(self._gameobjects))])
            if event.type == pygame.QUIT:
                return False
        self.targetboid.position = pygame.mouse.get_pos()
        for gameobjs in self._gameobjects:
            if type(gameobjs) == boids.Agent:
                if self.flee:
                    gameobjs.scared = True
                else:
                    gameobjs.scared = False
                if self.wander:
                    gameobjs.bored = True
                else:
                    gameobjs.bored = False
                if not self.wander:
                    gameobjs.target = self.targetboid
            gameobjs.update(self.deltatime)
        return True

    def draw(self):
        """Draw all gameobjects added to this game."""
        for gameobj in self._gameobjects:
            gameobj.draw(self.surface)
        test = "\'spacebar to spawn an agent\'    \'s to Seek\'"
        test = test + "     \'w to Wander\'    \'f to Flee\'"
        fps = "fps: {},  objects in game: {}".format(
            int(math.floor(self.clock.get_fps())), len(self._gameobjects))
        fpstext = self.font.render(fps, True, (255, 255, 255))
        testthing = self.font.render(test, True, (255, 255, 255))
        self.surface.blit(testthing, (0, 0))
        self.surface.blit(fpstext, (0, 20))
        super(ConcreteGame, self).draw()

    def run(self):
        """Need documentation."""
        if super(ConcreteGame, self).startup():
            while self.update():
                self.draw()
        super(ConcreteGame, self).shutdown()
