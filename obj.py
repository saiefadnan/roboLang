class Obj:
    def __init__(self, name, world, x, y, simulator=None):
        self.name = name
        self.world = world
        self.x = x
        self.y = y
        self.simulator = simulator

        if self.isWithinWorld():
            print(f"{self.name} spawned at ({self.x}, {self.y})")
            if self.simulator:
                self.simulator.spawn_obj(self.name, self.x, self.y)
        else:
            print(f"{self.name} is outside the world")

    def movX(self, value):
        self.x += value
        if self.isWithinWorld():
            print(f"{self.name} moved X to ({self.x}, {self.y})")
            if self.simulator:
                self.simulator.move_obj(self.name, self.x, self.y)
        else:
            print(f"{self.name} is outside the world")
    
    def movY(self, value):
        self.y += value
        if self.isWithinWorld():
            print(f"{self.name} moved Y to ({self.x}, {self.y})")
            if self.simulator:
                self.simulator.move_obj(self.name, self.x, self.y)
        else:
            print(f"{self.name} is outside the world")
    
    def isWithinWorld(self):
        return self.x >= 0 and self.x <= self.world.x and self.y >= 0 and self.y <= self.world.y