from parser import Parser
from lexer import Lexer

code = "movX(10) movY(90)"
lexer = Lexer(code)
parser = Parser(lexer)
ast = parser.parse()
print(ast)


# [movXNode(10), movYNode(90)]