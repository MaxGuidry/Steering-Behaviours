"""Class Boid."""
import math
import random

import pygame

import vectoroperations as vec


class Agent(object):
    """Class Agent."""

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=no-member
    # pylint: disable=too-many-function-args

    def __init__(self, positionbound, base, height):
        """Constructor."""
        self.position = (positionbound[0] / 2, positionbound[1] / 2)
        self.velocity = (random.randrange(-400, 400),
                         random.randrange(-400, 400))
        self.heading = (1, 0)
        self.acceleration = (0, 0)
        self.maxvelo = 200
        self.target = None
        self.forceapplied = (0, 0)
        self.bounds = positionbound
        self.wandertimer = 1
        self.wanderangle = 0
        self.scared = False
        self.bored = True
        self.surface = pygame.Surface((base, height), pygame.SRCALPHA)
        self.mass = (.5 * self.surface.get_width() * self.surface.get_height()) / 1875
        pygame.draw.line(self.surface, (0,
                                        random.randrange(100, 256),
                                        random.randrange(0, 150)),
                         (0, 0), (base, height / 2), 3)
        pygame.draw.line(self.surface, (0,
                                        random.randrange(100, 256),
                                        random.randrange(0, 150)),
                         (base, height / 2), (0, height), 3)
        pygame.draw.line(self.surface, (0,
                                        random.randrange(100, 256),
                                        random.randrange(0, 150)),
                         (0, height), (0, 0), 3)
    def updatealone(self, deltatime):
        """Update function for agents."""
        if self.scared:
            self._addforce((self.flee()[0] * 1, self.flee()[1] * 1))
            self.wandertimer = 1
        elif self.bored:
            # self._addforce(self.wander(90, 90))
            self._addforce((self.wandermax(self.mass)[0], self.wandermax(self.mass)[1]))
            self.wandertimer += deltatime
        else:
            self._addforce((self.seek()[0] * 1, self.seek()[1] * 1))
            self.wandertimer = 1
        self._updateacceleration()
        self._updatevelocity(deltatime)
        self._updateposition(deltatime)

    def update(self, deltatime):
        """Update function for agents."""
        if self.scared:
            self._addforce((self.flee()[0] * 1, self.flee()[1] * 1))
            self._addforce((self.seek()[0] * 0, self.seek()[1] * 0))
            self._addforce((self.wandermax(self.mass)[0] * 1, self.wandermax(self.mass)[1] * 1))
        elif self.bored:
            #self._addforce(self.wander(90, 90))
            self._addforce((self.flee()[0] / 128, self.flee()[1] / 128))
            self._addforce((self.seek()[0] / 128, self.seek()[1] / 128))
            self._addforce((self.wandermax(self.mass)[0], self.wandermax(self.mass)[1]))
        else:
            # self._addforce(self.wander(90, 90))
            self._addforce((self.flee()[0] * 0, self.flee()[1] * 0))
            self._addforce((self.seek()[0] * 1, self.seek()[1] * 1))
            self._addforce((self.wandermax(self.mass)[0], self.wandermax(self.mass)[1]))
        self.wandertimer += deltatime
        self._updateacceleration()
        self._updatevelocity(deltatime)
        self._updateposition(deltatime)

    def draw(self, screen):
        """Draw function for agents."""
        self.heading = vec.get_normalized(self.velocity)
        copy = pygame.transform.rotate(
            self.surface, -1 * (180 * math.atan2(self.heading[1],
                                                 self.heading[0])) / math.pi)
        screen.blit(copy, self.position)

    def seek(self):
        """Seeking Behaviour."""
        displacement = vec.get_dist(self.position, self.target.position)
        direction = vec.get_normalized(displacement)
        if vec.get_magnitude(displacement) == 0:
            return self.flee()
        return(direction[0] * vec.get_magnitude(displacement),
               direction[1] *
               vec.get_magnitude(displacement))

    def flee(self):
        """Flee behavior."""
        displacement = vec.get_dist(self.position, self.target.position)
        direction = vec.get_normalized(displacement)
        if vec.get_magnitude(displacement) != 0:
            return(direction[0] * ((1 /
                                    vec.get_magnitude(displacement))
                                   * self.bounds[0] * self.bounds[0])
                   * -.1,
                   direction[1] * ((1 /
                                    vec.get_magnitude(displacement))
                                   * self.bounds[1] * self.bounds[1])
                   * -.1)
        else:
            return (0, 0)

    def wander(self, distance, radius):
        """Correct wander Behaviour."""
        center_circle = vec.get_normalized(self.velocity)
        center_circle = (center_circle[0] * distance,
                         center_circle[1] * distance)
        displacement = (0, radius)
        self.wanderangle += (random.random() * 1) - (1 * .5)
        displacement = (math.cos(self.wanderangle) *
                        vec.get_magnitude(displacement),
                        math.sin(self.wanderangle) *
                        vec.get_magnitude(displacement))
        return (center_circle[0] + displacement[0],
                center_circle[1] + displacement[1])

    def wandermax(self, strength):
        """Behaviour that wanders."""
        time = random.uniform(.2, .4)
        if self.wandertimer > time:
            self.wandertimer = 0
            angle = -60
            self.wanderangle = angle + random.randrange(0, 120)
            currentangle = math.atan2(
                self.heading[1], self.heading[0]) * (180 / math.pi)
            currentangle += self.wanderangle
            direction = (math.cos((currentangle / 180) * math.pi),
                         math.sin((currentangle / 180) * math.pi))
            self.target.position = ((self.position[0] + direction[0]),
                                    (self.position[1] + direction[1]))
        currentangle = math.atan2(
            self.heading[1], self.heading[0]) * (180 / math.pi)
        currentangle += self.wanderangle
        direction = (math.cos((currentangle / 180) * math.pi),
                     math.sin((currentangle / 180) * math.pi))
        self.heading = direction
        self.target.position = (self.position[0] + direction[0],
                                self.position[1] + direction[1])
        forcetoadd = self.seek()
        forcetoadd = (forcetoadd[0] * self.maxvelo * strength,
                      forcetoadd[1] * self.maxvelo * strength)
        return forcetoadd

    def settarget(self, target):
        """Set the target of the agent."""
        self.target = target

    def _addforce(self, forceapplied):
        if forceapplied is None:
            return
        self.forceapplied = (self.forceapplied[0] + forceapplied[0],
                             self.forceapplied[1] + forceapplied[1])

    def _updateacceleration(self):
        self.acceleration = (self.forceapplied[0] / self.mass,
                             self.forceapplied[1] / self.mass)
        self.forceapplied = (0, 0)

    def _updatevelocity(self, deltatime):
        self.velocity = ((self.velocity[0]) + self.acceleration[0] * deltatime,
                         (self.velocity[1]) + self.acceleration[1] * deltatime)
        if vec.get_magnitude(self.velocity) > self.maxvelo:
            self.velocity = (vec.get_normalized(self.velocity)[0] *
                             self.maxvelo, vec.get_normalized(self.velocity)[1]
                             * self.maxvelo)

    def _updateposition(self, deltatime):
        self.position = ((self.position[0]) + self.velocity[0] * deltatime,
                         (self.position[1]) + self.velocity[1] * deltatime)
        if self.position[0] < -100:
            self.position = (self.bounds[0] / 2, self.bounds[1] / 2)
        if self.position[1] < -100:
            self.position = (self.bounds[0] / 2, self.bounds[1] / 2)
        if self.position[0] > self.bounds[0] + 100:
            self.position = (self.bounds[0] / 2, self.bounds[1] / 2)
        if self.position[1] > self.bounds[1] + 100:
            self.position = (self.bounds[0] / 2, self.bounds[1] / 2)
