from parser import Parser
from lexer import Lexer
from interpreter import Interpreter
from world import World
from simulator import Simulator
import turtle

with open("nano.rl", "r") as f:
    code = f.read()

if len(code) == 0:
    print("Error: Empty source code")
    exit()

lexer = Lexer(code)
parser = Parser(lexer)
ast = parser.parse()

# First visit to get the world for simulator setup
# Actually, we can just look for the world node in AST
world_node = None
for node_item in ast:
    if node_item[0] == "world":
        world_node = node_item[1]
        break

if world_node is None:
    print("Error: World not defined in source code")
    exit()

world_obj = World(world_node.x, world_node.y)

# Initialize simulator with the world object
simulator = Simulator(world_obj)

# Initialize interpreter with simulator
interpreter = Interpreter(lexer, simulator)
# Pre-set the world in interpreter vars so it doesn't try to create a new one without simulator
interpreter.vars["world"] = world_obj

print("Starting interpretation...")
for node in ast:
    # Skip world node as we already used it, or let interpreter handle it
    interpreter.visit(node)

print("Interpretation finished.")
# Keep turtle window open
turtle.done()
