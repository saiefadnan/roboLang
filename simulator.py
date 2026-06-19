from compiler import idToName
import turtle

class Simulator:
    def __init__(self, world):
        self.world = world
        self.screen = turtle.Screen()
        self.screen.title("roboLang Visualization")
        self.screen.setup(world.x + 50, world.y + 50)
        self.screen.setworldcoordinates(0, 0, world.x, world.y)
        self.objs = {}

    def spawn_obj(self, id, x, y):
        name = idToName[id]
        obj = turtle.Turtle()
        obj.shape("circle")
        obj.penup()
        obj.goto(x, y)
        obj.pendown()
        obj.write(name, align="center", font=("Arial", 12, "normal"))
        self.objs[id] = obj
        print(f"Visualization: {id} spawned at ({x}, {y})")

    def move_obj(self, id, x, y):
        if id in self.objs:
            self.objs[id].goto(x, y)
            print(f"Visualization: {id} moved to ({x}, {y})")

    def run(self):
        # Keep the window open
        print("Visualization running... close window to exit.")
        # self.screen.mainloop() is usually called at the end, but since we are running step by step
        # we might just want to update it.
        pass

    def update(self):
        self.screen.update()
