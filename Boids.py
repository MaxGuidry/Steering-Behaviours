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

    def __init__(self, positionbound):
        """Constructor."""
        self.position = (0, 0)
        self.velocity = (100, 100)
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
        """Update function for agents."""
        if self.scared:
            self._addforce(self.flee())
        elif self.bored:
            self._addforce(self.wander(deltatime))
        else:
            self.maxvelo = 200
            self._addforce(self.seek())
            self.wandertimer = 1
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
        return(direction[0] * vec.get_magnitude(displacement) * 4,
               direction[1] *
               vec.get_magnitude(displacement) * 4)

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

    # def otherwander(self, radius, dist, jitter, strength):
    #     """The correct way to wander."""
    #     return None

    def wander(self, deltatime):
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
            #self.target = Agent((999999, 999999))
            self.target.position = ((self.position[0] + direction[0]),
                                    (self.position[1] + direction[1]))
        self.wandertimer += deltatime
        currentangle = math.atan2(
            self.heading[1], self.heading[0]) * (180 / math.pi)
        currentangle += self.wanderangle
        direction = (math.cos((currentangle / 180) * math.pi),
                     math.sin((currentangle / 180) * math.pi))
        self.heading = direction
        self.target.position = (self.position[0] + direction[0],
                                self.position[1] + direction[1])
        forcetoadd = self.seek()
        forcetoadd = (forcetoadd[0] * 45, forcetoadd[1] * 45)
        return forcetoadd

    def settarget(self, target):
        """Set the target of the agent."""
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

    def _addforce(self, forceapplied):
        if forceapplied is None:
            return
        self.forceapplied = (self.forceapplied[0] + forceapplied[0],
                             self.forceapplied[1] + forceapplied[1])

    def _updateacceleration(self):
        self.acceleration = (self.forceapplied[0],
                             self.forceapplied[1])
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
        # if self.position[0] < -50:
        #     self.position = (self.bounds[0] / 2, self.bounds[1] / 2)
        # if self.position[1] < -30:
        #     self.position = (self.bounds[0] / 2, self.bounds[1] / 2)
        # if self.position[0] > self.bounds[0] + 30:
        #     self.position = (self.bounds[0] / 2, self.bounds[1] / 2)
        # if self.position[1] > self.bounds[1] + 30:
        #     self.position = (self.bounds[0] / 2, self.bounds[1] / 2)
