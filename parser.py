from lexer import TOKEN_COMMENT, TOKEN_NEWLINE, TOKEN_VARIABLE, TOKEN_DOT, TOKEN_EOF, TOKEN_COMMA, TOKEN_LPAREN, TOKEN_RPAREN, TOKEN_STRING, TOKEN_NUMBER
from commandnode import CommandNode
from registry import TOKEN_TO_CONFIG

class Parser():
    def __init__(self, lexer):
        self.lexer = lexer
        self.curr_token = lexer.get_next_token()
    
    def error(self, msg="Invalid token"):
        raise SyntaxError(f"Parser error at position {self.lexer.pos}: {msg}")
    
    def eat(self, token_type):
        if self.curr_token[0] == token_type:
            self.curr_token = self.lexer.get_next_token()
        else:
            self.error(f"Expected {token_type}, got {self.curr_token[0]}: {self.curr_token}")

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

    def parse_arg(self, expected_type):
        if self.curr_token[0] == TOKEN_NUMBER and expected_type == "int":
            return self.expect_number()
        elif self.curr_token[0] == TOKEN_STRING and expected_type == "str":
            return self.expect_string()
        elif self.curr_token[0] == TOKEN_VARIABLE:
            name = self.curr_token[1]
            self.eat(TOKEN_VARIABLE)
            if self.curr_token[0] == TOKEN_DOT:
                self.eat(TOKEN_DOT)
                prop = self.curr_token[1]
                self.eat(TOKEN_VARIABLE)
                return {"type": "variable_prop", "name": name, "prop": prop}
            return {"type": "variable", "name": name}
        else:
            self.error(f"Expected {expected_type}, got {self.curr_token[0]}")

    def parse_command(self, obj_name, config):
        self.eat(config["token"])
        args = []
        arg_types = config.get("arg_types", [])
        
        if len(arg_types) > 0:
            self.eat("LPAREN")
            for i, expected_type in enumerate(arg_types):
                args.append(self.parse_arg(expected_type))
                if i < len(arg_types) - 1:
                    self.eat("COMMA")
            self.eat("RPAREN")
        elif self.curr_token[0] == "LPAREN": # Optional empty parens
            self.eat("LPAREN")
            if(self.curr_token[0]==TOKEN_VARIABLE):
                self.eat(TOKEN_VARIABLE)
                args.append(self.expect_number())
            self.eat("RPAREN")
        if config.get("block", False):
            nodes = self.parse_block()
            return CommandNode(obj_name, config["name"], args, nodes)
            
        return CommandNode(obj_name, config["name"], args)

    def parse_block(self):
        self.eat("LBRACE")
        nodes = []
        while self.curr_token[0] != "RBRACE":
            self.run(nodes)
        self.eat("RBRACE")
        print(f"this is it {nodes}")
        return nodes

    def parse_newline(self):
        self.eat("NEWLINE")
        return []
    
    def parse_comment(self):
        self.eat("COMMENT")
        while self.curr_token[0] != TOKEN_EOF and self.curr_token[0] != TOKEN_NEWLINE:
            self.curr_token = self.lexer.get_next_token()
        return []

    def commandOrValue(self):
        if self.curr_token[0] == TOKEN_VARIABLE:
            obj_name = self.parse_obj_prefix()
            cmd_token = self.curr_token[0]
            if cmd_token in TOKEN_TO_CONFIG:
                config = TOKEN_TO_CONFIG[cmd_token]
                rhs = self.parse_command(obj_name, config)
            else:
                self.error(f"Unknown command '{cmd_token}'")
        elif self.curr_token[0] == "NUMBER":
            rhs = self.expect_number()
        elif self.curr_token[0] == "STRING":
            rhs = self.expect_string()
        else:
            self.error(f"Unexpected token {self.curr_token[0]} in assignment")
        return rhs

    def command(self, nodes):
        token_type = self.curr_token[0]
        config = TOKEN_TO_CONFIG[token_type]
        nodes.append(self.parse_command(config.get("default_obj", "global"), config))

    def newline(self, nodes):
        token_type = self.curr_token[0]
        if token_type == TOKEN_NEWLINE:
            self.parse_newline()
            nodes.append(CommandNode("newline", "skip", []))
            return True
        return False


    def comment(self, nodes):
        token_type = self.curr_token[0]
        if token_type == TOKEN_COMMENT:
            self.parse_comment()
            nodes.append(CommandNode("comment", "skip", []))
            return True
        return False


    def run(self, nodes):
        token_type = self.curr_token[0]
        
        if(self.comment(nodes)):
            return
        if(self.newline(nodes)):
            return

        if token_type == "VAR":
            # Assignment: var hello = r2.getPos()
                self.eat("VAR")
                var_name = self.curr_token[1]
                self.eat(TOKEN_VARIABLE)
                self.eat("EQ")
                rhs = self.commandOrValue()
                nodes.append(CommandNode(var_name, "assign", [rhs]))

        elif token_type == TOKEN_VARIABLE:
            nodes.append(self.commandOrValue())

        elif token_type in TOKEN_TO_CONFIG:
            self.command(nodes)
            
        else:
            self.error(f"Unexpected token {token_type}")

        return nodes
        

    def parse(self):
        nodes = []
        while self.curr_token[0] != TOKEN_EOF:
           self.run(nodes)
        return nodes
