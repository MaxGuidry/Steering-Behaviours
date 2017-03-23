"""Class Boid."""
import vectoroperations as vec
import random
import math


class Boid(object):
    """Class Boid."""

    def __init__(self, positionbound):
        self.position = (0, 0)
        self.velocity = (0, 0)
        self.acceleration = (0, 0)
        self.maxvelo = 10
        self.target = None
        self.forceapplied = (0, 0)
        self.bounds = positionbound
        self.wandertimer = 0

    def seek(self, scalingfactor):
        """Seeking Behaviour."""
        displacement = vec.get_dist(self.position, self.target.position)
        direction = vec.get_normalized(displacement)
        if vec.get_magnitude(displacement) == 0:
            self.flee(scalingfactor * 2)
        self._addforce((direction[0] * vec.get_magnitude(displacement) * 200, direction[1] * vec.get_magnitude(displacement) * 200))
        self._updateacceleration(scalingfactor)
        self._updatevelocity(scalingfactor)
        self._updateposition()

    def flee(self, scalingfactor):
        displacement = vec.get_dist(self.position, self.target.position)
        direction = vec.get_normalized(displacement)
        if vec.get_magnitude(displacement) != 0:
            self._addforce((direction[0] * ((1 / vec.get_magnitude(displacement)) * self.bounds[0] * self.bounds[0]) * -200, direction[1] * ((1 / vec.get_magnitude(displacement)) * self.bounds[1] * self.bounds[1]) * -200))
        self._updateacceleration(scalingfactor)
        self._updatevelocity(scalingfactor)
        self._updateposition()

    def wander(self, scalingfactor):
        time = random.uniform(0.3, 0.6)
        if self.wandertimer > time:
            self.wandertimer = 0
            degree = random.choice((30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360))
            offset = random.randrange(1, 30)
            degree += offset
            print degree
            direction = (math.sin((degree * math.pi) / 180), math.cos((degree * math.pi) / 180))
            self.target = Boid((99999, 99999))
            self.target.position = (self.position[0] + direction[0], self.position[1] + direction[1])
        previousposition = self.position
        self.wandertimer += scalingfactor
        self.maxvelo = 5
        #self._addforce(vec.get_normalized((self.bounds[0] / 2, self.bounds[1] / 2)))
        self.seek(scalingfactor * 20)
        newpositioin = self.position
        deltaposition = (newpositioin[0] - previousposition[0], newpositioin[1] - previousposition[1])
        self.target.position = (self.position[0] + deltaposition[0], self.position[1] + deltaposition[1])
        # self.target.position = (self.position[0] + (direction + heading))

        #self._addforce((vec.get_normalized((direction[0] + heading[0], direction[1] + heading[1]))[0] * 600, vec.get_normalized((direction[0] + heading[0], direction[1] + heading[1]))[1] * 600))
        #self._updateacceleration(scalingfactor)
        #self._updatevelocity(scalingfactor)
        #self._updateposition()

    def arrive(self, scalingfactor):
        pass

    def pursue(self, scalingfactor):
        pass

    def evade(self, scalingfactor):
        pass

    def centerofmass(self, boids):
        com = (0, 0)
        for b in boids:
            if b != self:
                com = (com[0] + b.position[0], com[1] + b.position[1])
        com = (com[0] / (len(boids) - 1), com[1] / (len(boids) - 1))
        self._addforce((vec.get_dist(com, self.position)[0] / 1, vec.get_dist(com, self.position)[1] / 1))

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
            self.velocity = (vec.get_normalized(self.velocity)[0] * self.maxvelo, vec.get_normalized(self.velocity)[1] * self.maxvelo)

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
