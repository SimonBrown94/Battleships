class Ship:
    """Create a ship"""

    def __init__(self, xpos, ypos, length, direction):
        self.xpos = xpos
        self.ypos = ypos
        self.length = length
        self.ship = ['S' for i in range(length)]
        self.direction = direction
        self.coords = []
        self.dead = False

        if direction == "h":
            for i in range(length):
                self.coords.append([self.xpos + i, self.ypos])
        else:
            for i in range(length):
                self.coords.append([self.xpos, self.ypos + i])

    def update_ship(self, position):
        # Determine if the attack was a hit or a sink
        self.ship[position] = 'h'
        if self.ship.count('h') == self.length:
            self.dead = True
            return "Sank!"
        else:
            return "Hit"
