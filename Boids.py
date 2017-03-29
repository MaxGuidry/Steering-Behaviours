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
        self.heading = (1, 0)
        self.acceleration = (0, 0)
        self.maxvelo = 10
        self.target = None
        self.forceapplied = (0, 0)
        self.bounds = positionbound
        self.forward = (1, 0)
        self.wandertimer = 1
        self.scared = False
        self.surface = pygame.Surface((75, 50), pygame.SRCALPHA)
        pygame.draw.line(self.surface, (0,
                                        random.randrange(100, 256),
                                        random.randrange(0, 150)),
                         (0, 0), (75, 25), 3)
        pygame.draw.line(self.surface, (0,
                                        random.randrange(100, 256),
                                        random.randrange(0, 150)),
                         (75, 25), (0, 50), 3)
        pygame.draw.line(self.surface, (0,
                                        random.randrange(100, 256),
                                        random.randrange(0, 150)),
                         (0, 50), (0, 0), 3)

    def update(self, deltatime):
        if vec.get_magnitude(vec.get_dist(self.position, self.target.position)) < 400 and self.target.bounds != (999999, 999999):
            self._addforce(self.seek(), deltatime)
            self.wandertimer = 1
        else:
            self._addforce(self.wander(deltatime), deltatime)

    def draw(self, screen):
        copy = pygame.transform.rotate(
            self.surface, -1 * (180 * math.atan2(self.heading[1], self.heading[0])) / math.pi)
        self.heading = vec.get_normalized(self.velocity)
        screen.blit(copy, self.position)

    def seek(self):
        """Seeking Behaviour."""
        displacement = vec.get_dist(self.position, self.target.position)
        direction = vec.get_normalized(displacement)
        if vec.get_magnitude(displacement) == 0:
            return self.flee()
        return(direction[0] * vec.get_magnitude(displacement) * 2000, direction[1] *
               vec.get_magnitude(displacement) * 2000)

    def flee(self):
        """Flee behavior."""
        displacement = vec.get_dist(self.position, self.target.position)
        direction = vec.get_normalized(displacement)
        if vec.get_magnitude(displacement) != 0:
            return(direction[0] * ((1 /
                                    vec.get_magnitude(displacement))
                                   * self.bounds[0] * self.bounds[0])
                   * -10,
                   direction[1] * ((1 /
                                    vec.get_magnitude(displacement))
                                   * self.bounds[1] * self.bounds[1])
                   * -10)
        else:
            return (0, 0)

    def otherwander(self, radius, dist, jitter, strength):
        return None

    def wander(self, deltatime):
        """Behaviour that wanders."""
        time = random.uniform(.6, .8)
        if self.wandertimer > time:
            self.wandertimer = 0
            degree = -60
            offset = random.randrange(1, 120)
            degree += offset
            currentangle = math.atan2(self.heading[1], self.heading[0]) * (180 / math.pi)
            currentangle += degree
            direction = (math.cos((currentangle / 180) * math.pi), math.sin((currentangle / 180) * math.pi))
            self.target = Agent((999999, 999999))
            self.target.position = ((self.position[0] + direction[0]),
                                    (self.position[1] + direction[1]))
        self.wandertimer += deltatime
        self.maxvelo = 3
        forcetoadd = self.seek()
        forcetoadd = (forcetoadd[0] * self.maxvelo,
                      forcetoadd[1] * self.maxvelo)
        newposfortarget = ((forcetoadd[0] * deltatime * deltatime) * 2 + self.position[0],
                           (forcetoadd[1] * deltatime * deltatime) * 2 + self.position[1])
        self.target.position = newposfortarget
        return forcetoadd

    def settarget(self, target):
        self.target = target

    def centerofmass(self, boids):
        """Calculate the center of mass of all agents."""
        com = (0, 0)
        for aboid in boids:
            if aboid != self:
                com = (com[0] + aboid.position[0], com[1] + aboid.position[1])
        com = (com[0] / (len(boids) - 1), com[1] / (len(boids) - 1))
        # self._addforce((vec.get_dist(com, self.position)[0] / 8,
        # vec.get_dist(com, self.position)[1] / 8))

    def _addforce(self, forceapplied, deltatime):
        if forceapplied is None:
            return
        self.forceapplied = (self.forceapplied[0] + forceapplied[0],
                             self.forceapplied[1] + forceapplied[1])
        self._updateacceleration(deltatime)
        self._updatevelocity(deltatime)
        self._updateposition(deltatime)

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

    def _updateposition(self, deltatime):
        self.position = (self.position[0] + self.velocity[0],
                         self.position[1] + self.velocity[1])
        if self.position[0] < 10:
            self.position = (10, self.position[1])
            self.position = (self.bounds[0] / 2, self.bounds[1] / 2)
        if self.position[1] < 10:
            self.position = (self.position[0], 10)
            self.position = (self.bounds[0] / 2, self.bounds[1] / 2)
        if self.position[0] > self.bounds[0] - 10:
            self.position = (self.bounds[0] - 10, self.position[1])
            self.position = (self.bounds[0] / 2, self.bounds[1] / 2)
        if self.position[1] > self.bounds[1] - 10:
            self.position = (self.position[0], self.bounds[1] - 10)
            self.position = (self.bounds[0] / 2, self.bounds[1] / 2)
