from lexer import Lexer

code = "movX(10) movY(10)"
lexer = Lexer(code)
token = lexer.get_next_token()

while token[0] != "EOF":
    print(token)
    token = lexer.get_next_token()

print(token)



# output:
# ('movX', 'movX')
# ('LPAREN', '(')
# ('NUMBER', 10)
# ('RPAREN', ')')
# ('movY', 'movY')
# ('LPAREN', '(')
# ('NUMBER', 90)
# ('RPAREN', ')')
# ('EOF', None)