from vm import VirtualMachine
from compiler import Compiler
from parser import Parser
from lexer import Lexer
from world import World
from simulator import Simulator
import turtle

with open("nano.rl", "r") as f:
    code = f.read()

if len(code) == 0:
    print("Error: Empty source code")
    exit()

lexer = Lexer(code)

# token = lexer.get_next_token()
# while token[0] != "EOF":
#     print(token)
#     token = lexer.get_next_token()

# print(token)

parser = Parser(lexer)
ast = parser.parse()

# print(ast)

# First visit to get the world for simulator setup
# Actually, we can just look for the world node in AST
world_node = None
for node_item in ast:
    if node_item.action == "world":
        world_node = node_item
        break

if world_node is None:
    print("Error: World not defined in source code")
    exit()

world = World(world_node.args[0], world_node.args[1])

# Initialize simulator with the world object
simulator = Simulator(world)

compiler = Compiler()
bytecode = compiler.compile(ast)

print(bytecode)

vm = VirtualMachine(simulator)
vm.run(bytecode)

turtle.done()
