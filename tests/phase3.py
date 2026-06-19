from obj import Robot
from parser import Parser
from lexer import Lexer
from interpreter import Interpreter

code = "movX(10) movY(90)"
lexer = Lexer(code)
parser = Parser(lexer)
ast = parser.parse()
robot = Robot(0,0)
interpreter = Interpreter(robot)

for node in ast:
    interpreter.visit(node)


# output

# Moving 10
# movYing 90