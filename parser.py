from lexer import TOKEN_COMMENT, TOKEN_NEWLINE, TOKEN_VARIABLE, TOKEN_DOT, TOKEN_EOF, TOKEN_COMMA, TOKEN_LPAREN, TOKEN_RPAREN, TOKEN_STRING
from commandnode import CommandNode
from registry import TOKEN_TO_CONFIG

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

    def expect_string(self):
        value = self.curr_token[1]
        self.eat("STRING")
        return value

    def parse_obj_prefix(self):
        obj = self.curr_token[1]
        self.eat("VARIABLE")
        self.eat("DOT")
        return obj

    def parse_command(self, obj_name, config):
        self.eat(config["token"])
        args = []
        arg_types = config.get("arg_types", [])
        
        if len(arg_types) > 0:
            self.eat("LPAREN")
            for i, expected_type in enumerate(arg_types):
                if expected_type == "int":
                    args.append(self.expect_number())
                elif expected_type == "str":
                    args.append(self.expect_string())
                else:
                    self.error(f"Unknown registry arg_type '{expected_type}'")
                
                if i < len(arg_types) - 1:
                    self.eat("COMMA")
            self.eat("RPAREN")
        elif self.curr_token[0] == "LPAREN": # Optional empty parens
            self.eat("LPAREN")
            self.eat("RPAREN")
            
        return CommandNode(obj_name, config["name"], args)

    def parse_newline(self):
        self.eat("NEWLINE")
        return []
    
    def parse_comment(self):
        self.eat("COMMENT")
        while self.curr_token[0] != TOKEN_EOF and self.curr_token[0] != TOKEN_NEWLINE:
            self.curr_token = self.lexer.get_next_token()
        return []

    def parse(self):
        nodes = []
        while self.curr_token[0] != TOKEN_EOF:
            token_type = self.curr_token[0]

            if token_type == TOKEN_COMMENT:
                self.parse_comment()
                nodes.append(CommandNode("comment", "skip", []))

            elif token_type == TOKEN_NEWLINE:
                self.parse_newline()
                nodes.append(CommandNode("newline", "skip", []))

            elif token_type == TOKEN_VARIABLE:
                obj_name = self.parse_obj_prefix()
                cmd_token = self.curr_token[0]
                if cmd_token in TOKEN_TO_CONFIG:
                    config = TOKEN_TO_CONFIG[cmd_token]
                    nodes.append(self.parse_command(obj_name, config))
                else:
                    self.error(f"Unknown command '{cmd_token}' after object '{obj_name}'")

            elif token_type in TOKEN_TO_CONFIG:
                config = TOKEN_TO_CONFIG[token_type]
                nodes.append(self.parse_command(config.get("default_obj", "global"), config))
            
            else:
                self.error(f"Unexpected token {token_type}")

        return nodes