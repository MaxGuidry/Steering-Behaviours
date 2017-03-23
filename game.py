"""Game file for update draw ect..."""


class Game(object):
    """Game control class."""

    def __init__(self):
        """Constructor."""
        self.batch = []

    def addtobatch(self, obj):
        """Add object to batch."""
        self.batch.append(obj)

    def start(self):
        """Start."""
        pass

    def update(self, deltatime):
        """Update."""
        pass

    def draw(self):
        """Draw."""
        pass

    def run(self):
        """Run."""
        pass

    def exit(self):
        """Exit."""
        pass
