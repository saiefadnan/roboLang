from world import World
from obj import Obj
from simulator import Simulator

class Interpreter:
    def __init__(self, lexer, simulator=None):
        self.lexer = lexer
        self.simulator = simulator
        self.vars = {}

    def error(self, msg="Invalid token"):
        raise SyntaxError(f"Interpreter error at position {self.lexer.pos}: {msg}")
    
    def visit(self, node):
        name = node.name
        action = node.action
        args = node.args

        if action == "movX":
            if name not in self.vars:
                self.error(f"Object '{name}' not initialized")
            self.vars[name].movX(args[0])
        elif action == "movY":
            if name not in self.vars:
                self.error(f"Object '{name}' not initialized")
            self.vars[name].movY(args[0])
        elif action == "init":
            if name in self.vars:
                self.error(f"Object '{name}' already initialized")
            if "world" not in self.vars:
                self.error("World must be initialized before objects")
            self.vars[name] = Obj(name, self.vars["world"], args[0], args[1], self.simulator)
        elif action == "create":
            world_obj = World(args[0], args[1])
            self.vars["world"] = world_obj
            if self.simulator is None:
                # We can initialize simulator here if needed, but better to pass it in
                pass
            print(f"World initialized: {args[0]}x{args[1]}")