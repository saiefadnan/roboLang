from commandnode import CommandNode
from lexer import TOKEN_WORLD
from lexer import TOKEN_VARIABLE
from lexer import TOKEN_INIT
from lexer import TOKEN_MOVY
from lexer import TOKEN_MOVX
from lexer import TOKEN_EOF


class Parser():
    def __init__(self, lexer):
        self.lexer = lexer
        self.curr_token = lexer.get_next_token()
    
    def error(self, msg="Invalid token"):
        raise SyntaxError(f"Parser error at position {self.lexer.pos}: {msg} ('{self.curr_token[0]}')")
    
    def eat(self, token_type):
        if self.curr_token[0] == token_type:
            self.curr_token = self.lexer.get_next_token()
        else:
            self.error(f"Expected {token_type}, got {self.curr_token[0]}")

    def expect_number(self):
        value = self.curr_token[1]
        self.eat("NUMBER")
        return value

    def parse_init(self):
        self.eat("INIT")
        self.eat("LPAREN")
        x = self.expect_number()
        self.eat("COMMA")
        y = self.expect_number()
        self.eat("RPAREN")
        return [x, y]

    def parse_movX(self):
        self.eat("MOVX")
        self.eat("LPAREN")
        x = self.expect_number()
        self.eat("RPAREN")
        return [x]
    
    def parse_movY(self):
        self.eat("MOVY")
        self.eat("LPAREN")
        y = self.expect_number()
        self.eat("RPAREN")
        return [y]
    
    def parse_obj(self):
        obj = self.curr_token[1]
        self.eat("VARIABLE")
        self.eat("DOT")
        return obj

    def parse_world(self):
        self.eat("WORLD")
        self.eat("LPAREN")
        x = self.expect_number()
        self.eat("COMMA")
        y = self.expect_number()
        self.eat("RPAREN")
        return [x, y]

    def parse(self):
        nodes = []
        while self.curr_token[0] != TOKEN_EOF:
            if self.curr_token[0] == TOKEN_VARIABLE:
                objName = self.parse_obj()
                if self.curr_token[0] == TOKEN_MOVX:
                    args = self.parse_movX()
                    nodes.append(CommandNode(objName, "movX", args))
                elif self.curr_token[0] == TOKEN_MOVY:
                    args = self.parse_movY()
                    nodes.append(CommandNode(objName, "movY", args))
                elif self.curr_token[0] == TOKEN_INIT:
                    args = self.parse_init()
                    nodes.append(CommandNode(objName, "init", args))
                else:
                    self.error("Invalid statement")
            elif self.curr_token[0] == TOKEN_WORLD:
                args = self.parse_world()
                nodes.append(CommandNode("world", "create", args))
            else:
                self.error("Invalid statement")
        return nodes