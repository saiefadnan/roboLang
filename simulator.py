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
        self.objs[id] = {
            "obj": obj,
            "x": x,
            "y": y 
        }
        print(f"Visualization: {name} spawned at ({x}, {y})")

    def move_obj(self, id, x, y):
        name = idToName[id] 
        if id in self.objs:
            self.objs[id]["obj"].goto(x, y)
            self.objs[id]={
                "obj": self.objs[id]["obj"],
                "x": x,
                "y": y
            }
            print(f"Visualization: {name} moved to ({x}, {y})")

    def run(self):
        # Keep the window open
        print("Visualization running... close window to exit.")
        # self.screen.mainloop() is usually called at the end, but since we are running step by step
        # we might just want to update it.
        pass

    def result(self):
        ids = list(self.objs.keys())

        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                obj1 = self.objs[ids[i]]
                obj2 = self.objs[ids[j]]

                if (
                    obj1["x"] == obj2["x"]
                    and
                    obj1["y"] == obj2["y"]
                ):
                    print(
                        f"{idToName[ids[i]]} and "
                        f"{idToName[ids[j]]} collided!!!"
                )
    def update(self):
        self.screen.update()
