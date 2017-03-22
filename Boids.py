"""Class Boid."""
import vectoroperations as vec


class Boid(object):
    """Class Boid."""

    def __init__(self):
        self.position = (0, 0)
        self.velocity = (0, 0)
        self.acceleration = (0, 0)
        self.maxvelo = 20
        self.target = None
        self.forceapplied = (0, 0)

    def seek(self, scalingfactor):
        """Seeking Behaviour."""
        displacement = vec.get_dist(self.position, self.target.position)
        direction = vec.get_normalized(displacement)
        self._addforce((direction[0] * 20000, direction[1] * 20000))
        self._updateacceleration(scalingfactor)
        self._updatevelocity(scalingfactor)
        self._updateposition()

    def flee(self, scalingfactor):
        pass

    def wander(self, scalingfactor):
        pass

    def arrive(self, scalingfactor):
        pass

    def pursue(self, scalingfactor):
        pass

    def evade(self, scalingfactor):
        pass

    def _addforce(self, forceapplied):
        self.forceapplied=(forceapplied[0],
                             forceapplied[1])

    def _updateacceleration(self, deltatime):
        self.acceleration = ((self.acceleration[0] + self.forceapplied[0]) * deltatime,
                             (self.acceleration[1] + self.forceapplied[1]) * deltatime)

    def _updatevelocity(self, deltatime):
        self.velocity = ((self.velocity[0] + self.acceleration[0]) * deltatime,
                         (self.velocity[1] + self.acceleration[1]) * deltatime)
        self.acceleration = (0, 0)
        if vec.get_magnitude(self.velocity) > self.maxvelo:
            self.velocity = (vec.get_normalized(self.velocity)[0] * self.maxvelo, vec.get_normalized(self.velocity)[1] * self.maxvelo)

    def _updateposition(self):
        self.position = (self.position[0] + self.velocity[0],
                         self.position[1] + self.velocity[1])
