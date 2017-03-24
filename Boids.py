"""Class Boid."""
import math
import random

import pygame

import vectoroperations as vec


class Agent(object):
    """Class Agent."""

    # pylint: disable=too-many-instance-attributes

    def __init__(self, positionbound):
        """Constructor."""
        self.position = (0, 0)
        self.velocity = (0, 0)
        self.acceleration = (0, 0)
        self.maxvelo = 10
        self.target = None
        self.forceapplied = (0, 0)
        self.bounds = positionbound
        self.wandertimer = 0

    def update(self, deltatime):
        pass

    def draw(self):
        testscreen = pygame.display.get_surface()
        pygame.draw.circle(pygame.display.get_surface(), (0,
                           random.randrange(100, 256),
                                    random.randrange(0, 150)),
                           (int(round(self.position[0])),
                            int(round(self.position[1]))), 10, 0)

    def seek(self, scalingfactor):
        """Seeking Behaviour."""
        displacement = vec.get_dist(self.position, self.target.position)
        direction = vec.get_normalized(displacement)
        if vec.get_magnitude(displacement) == 0:
            self.flee(scalingfactor * 2)
        self._addforce((direction[0] * self.maxvelo * 2000, direction[1] *
                        self.maxvelo * 2000))
        self._updateacceleration(scalingfactor)
        self._updatevelocity(scalingfactor)
        self._updateposition()

    def flee(self, scalingfactor):
        """Flee behavior."""
        displacement = vec.get_dist(self.position, self.target.position)
        direction = vec.get_normalized(displacement)
        if vec.get_magnitude(displacement) != 0:
            self._addforce((direction[0] * ((1 /
                                             vec.get_magnitude(displacement))
                                            * self.bounds[0] * self.bounds[0])
                            * -10,
                            direction[1] * ((1 /
                                             vec.get_magnitude(displacement))
                                            * self.bounds[1] * self.bounds[1])
                            * -10))
        self._updateacceleration(scalingfactor)
        self._updatevelocity(scalingfactor)
        self._updateposition()

    def wander(self, scalingfactor):
        """Behaviour that wanders."""
        time = random.uniform(0.3, 0.6)
        if self.wandertimer > time:
            self.wandertimer = 0
            degree = random.choice((30, 60, 90, 120, 150, 180, 210, 240,
                                    270, 300, 330, 360))
            offset = random.randrange(1, 30)
            degree += offset
            direction = (math.sin((degree * math.pi) / 180),
                         math.cos((degree * math.pi) / 180))
            self.target = Agent((999999, 999999))
            self.target.position = ((self.position[0] + direction[0]) * 1,
                                    (self.position[1] + direction[1]) * 1)
        previousposition = self.position
        self.wandertimer += scalingfactor
        self.maxvelo = 5
        self.seek(scalingfactor * 1)
        newpositioin = self.position
        deltaposition = ((newpositioin[0] - previousposition[0]) * 1,
                         (newpositioin[1] - previousposition[1]) * 1)
        self.target.position = ((self.position[0] + deltaposition[0]) * 1,
                                (self.position[1] + deltaposition[1]) * 1)

    def centerofmass(self, boids):
        """Calculate the center of mass of all agents."""
        com = (0, 0)
        for aboid in boids:
            if aboid != self:
                com = (com[0] + aboid.position[0], com[1] + aboid.position[1])
        com = (com[0] / (len(boids) - 1), com[1] / (len(boids) - 1))
        # self._addforce((vec.get_dist(com, self.position)[0] / 8,
        # vec.get_dist(com, self.position)[1] / 8))

    def _addforce(self, forceapplied):
        self.forceapplied = (self.forceapplied[0] + forceapplied[0],
                             self.forceapplied[1] + forceapplied[1])

    def _updateacceleration(self, deltatime):
        self.acceleration = (self.forceapplied[0] * deltatime,
                             self.forceapplied[1] * deltatime)
        self.forceapplied = (0, 0)

    def _updatevelocity(self, deltatime):
        self.velocity = ((self.velocity[0] + self.acceleration[0]) * deltatime,
                         (self.velocity[1] + self.acceleration[1]) * deltatime)
        if vec.get_magnitude(self.velocity) > self.maxvelo:
            self.velocity = (vec.get_normalized(self.velocity)[0] *
                             self.maxvelo, vec.get_normalized(self.velocity)[1]
                             * self.maxvelo)

    def _updateposition(self):
        self.position = (self.position[0] + self.velocity[0],
                         self.position[1] + self.velocity[1])
        if self.position[0] < 10:
            self.position = (10, self.position[1])
        if self.position[1] < 10:
            self.position = (self.position[0], 10)
        if self.position[0] > self.bounds[0] - 10:
            self.position = (self.bounds[0] - 10, self.position[1])
        if self.position[1] > self.bounds[1] - 10:
            self.position = (self.position[0], self.bounds[1] - 10)
