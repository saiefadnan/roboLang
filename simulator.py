from compiler import idToName
import turtle

class PosResult:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"Pos(x={self.x}, y={self.y})"

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
        
        label = turtle.Turtle()
        label.hideturtle()
        label.penup()
        label.goto(x, y + 15)
        label.write(name, align="center", font=("Arial", 12, "normal"))

        self.objs[id] = {
            "obj": obj,
            "x": x,
            "y": y 
        }
        print(f"Visualization: {name} spawned at ({x}, {y})")

    def move_obj_x(self, id, dx):
        name = idToName[id] 
        if id in self.objs:
            self.objs[id]["x"] += dx
            self.objs[id]["obj"].setx(self.objs[id]["x"])
            print(f"Visualization: {name} moved X by {dx} to {self.objs[id]['x']}")

    def move_obj_y(self, id, dy):
        name = idToName[id] 
        if id in self.objs:
            self.objs[id]["y"] += dy
            self.objs[id]["obj"].sety(self.objs[id]["y"])
            print(f"Visualization: {name} moved Y by {dy} to {self.objs[id]['y']}")

    def create_world(self, x, y):
        print(f"Visualization: World confirmed at {x}x{y}")

    def run(self):
        print("Visualization running... close window to exit.")
        pass

    def result(self):
        print("\nCollision Report:")
        ids = list(self.objs.keys())
        collided = False
        
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
               if(self.get_pos(ids[i]) == self.get_pos(ids[j])):
                   print(f"{idToName[ids[i]]} and {idToName[ids[j]]} collided!!!")
                   collided = True
        if not collided:
            print("No collisions detected.")

    def patrol(self, id, duration):
        name = idToName[id]
        print(f"Visualization: {name} starting patrol for {duration} seconds!")

    def say(self, id, message):
        name = idToName[id]
        print(f"[{name}] says: {message}")

    def get_pos(self, id):
        name = idToName[id]
        x = self.objs[id]['x']
        y = self.objs[id]['y']
        print(f"[{name}] position recorded: ({x}, {y})")
        return PosResult(x, y)

    def repeat(self, count):
        print(f"Repeating {count} times")
    
    def show(self, value):
        print(f"DISPLAY: {value}")
        
    def update(self):
        self.screen.update()
