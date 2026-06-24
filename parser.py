from lexer import TOKEN_MINUS
from lexer import (
    TOKEN_COMMENT, TOKEN_NEWLINE, TOKEN_VARIABLE, TOKEN_DOT,
    TOKEN_EOF, TOKEN_COMMA, TOKEN_LPAREN, TOKEN_RPAREN,
    TOKEN_STRING, TOKEN_NUMBER, TOKEN_EQ
)
from commandnode import CommandNode
from registry import TOKEN_TO_CONFIG

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.curr_token = lexer.get_next_token()

    def extract_sign(self):
        sign = 1
        if self.curr_token[0] == TOKEN_MINUS:
            self.eat(TOKEN_MINUS)
            sign = -1
        return sign    

    def error(self, msg="Invalid token"):
        raise SyntaxError(f"Parser error at position {self.lexer.pos}: {msg}")

    def eat(self, token_type):
        if self.curr_token[0] == token_type:
            self.curr_token = self.lexer.get_next_token()
        else:
            self.error(f"Expected '{token_type}', got '{self.curr_token[0]}': {self.curr_token}")

    # --- Primitive parsers ---

    def expect_number(self, sign):
        value = sign * self.curr_token[1]
        self.eat("NUMBER")
        return value

    def expect_string(self):
        value = self.curr_token[1]
        self.eat("STRING")
        return value

    def parse_obj_prefix(self):
        """Consume `identifier.` and return the identifier name."""
        obj = self.curr_token[1]
        self.eat("VARIABLE")
        self.eat("DOT")
        return obj

    # --- Argument parsing ---

    def parse_arg(self, expected_type=None):
        """
        Parse one argument. Accepts:
          - integer literal  (expected_type == "int" or None)
          - string literal   (expected_type == "str" or None)
          - variable         (any expected_type)
          - variable.prop    (any expected_type)
        """  
        sign = self.extract_sign()

        tok = self.curr_token[0]
        if tok == TOKEN_NUMBER:
            return self.expect_number(sign)

        if tok == TOKEN_STRING:
            return self.expect_string()

        if tok == TOKEN_VARIABLE:
            name = self.curr_token[1]
            self.eat(TOKEN_VARIABLE)
            if self.curr_token[0] == TOKEN_DOT:
                self.eat(TOKEN_DOT)
                prop = self.curr_token[1]
                self.eat(TOKEN_VARIABLE)
                return {"type": "variable_prop", "name": name, "prop": prop, "sign": sign}
            return {"type": "variable", "name": name, sign: sign}

        self.error(f"Expected argument (int/str/variable), got '{tok}'")

    # --- Block / command parsing ---

    def parse_block(self):
        """Parse `{ statement* }` and return the list of inner nodes."""
        self.eat("LBRACE")
        nodes = []
        while self.curr_token[0] not in ("RBRACE", TOKEN_EOF):
            self._parse_statement(nodes)
        self.eat("RBRACE")
        return nodes

    def parse_command(self, obj_name, config):
        """Parse a single command call based on its registry config."""
        self.eat(config["token"])
        args = []
        arg_types = config.get("arg_types", [])

        if arg_types:
            self.eat("LPAREN")
            for i, expected_type in enumerate(arg_types):
                args.append(self.parse_arg(expected_type))
                if i < len(arg_types) - 1:
                    self.eat("COMMA")
            self.eat("RPAREN")
        elif self.curr_token[0] == "LPAREN":
            # Command takes no declared args but may have parentheses
            self.eat("LPAREN")
            self.eat("RPAREN")

        if config.get("block", False):
            body = self.parse_block()
            return CommandNode(obj_name, config["name"], args, body)

        return CommandNode(obj_name, config["name"], args)

    # --- Statement parsing helpers ---

    def _skip_newlines_and_comments(self, nodes):
        """Returns True if a newline or comment was consumed."""
        tok = self.curr_token[0]
        if tok == TOKEN_NEWLINE:
            self.eat(TOKEN_NEWLINE)
            return True
        if tok == TOKEN_COMMENT:
            self.eat(TOKEN_COMMENT)
            # Skip the rest of the comment line
            while self.curr_token[0] not in (TOKEN_EOF, TOKEN_NEWLINE):
                self.curr_token = self.lexer.get_next_token()
            return True
        return False

    def _parse_var_decl(self, nodes):
        """Parse `var name = <rhs>`."""
        self.eat("VAR")
        var_name = self.curr_token[1]
        self.eat(TOKEN_VARIABLE)
        self.eat("EQ")
        rhs = self._parse_rhs()
        nodes.append(CommandNode(var_name, "assign", [rhs]))

    def _parse_rhs(self):
        """Parse the right-hand side of an assignment."""
        sign = self.extract_sign()
        tok = self.curr_token[0]
        if tok == TOKEN_VARIABLE:
            # Could be `obj.command(...)` or a bare variable / variable.prop
            name = self.curr_token[1]
            self.eat(TOKEN_VARIABLE)
            if self.curr_token[0] == TOKEN_DOT:
                self.eat(TOKEN_DOT)
                cmd_tok = self.curr_token[0]
                if cmd_tok in TOKEN_TO_CONFIG:
                    config = TOKEN_TO_CONFIG[cmd_tok]
                    return self.parse_command(name, config)
                else:
                    # variable.prop access
                    prop = self.curr_token[1]
                    self.eat(TOKEN_VARIABLE)
                    return {"type": "variable_prop", "name": name, "prop": prop, "sign": sign}
            return {"type": "variable", "name": name, "sign": sign}
        if tok == TOKEN_NUMBER:
            return self.expect_number(sign)
        if tok == TOKEN_STRING:
            return self.expect_string()
        self.error(f"Unexpected token '{tok}' in assignment")

    def _parse_statement(self, nodes):
        """Parse one statement and append result node(s) to `nodes`."""
        tok = self.curr_token[0]

        if self._skip_newlines_and_comments(nodes):
            return

        if tok == "VAR":
            self._parse_var_decl(nodes)
            return

        if tok == TOKEN_VARIABLE:
            # Object method call: `r1.movX(10)`
            obj_name = self.parse_obj_prefix()
            cmd_tok = self.curr_token[0]
            if cmd_tok in TOKEN_TO_CONFIG:
                config = TOKEN_TO_CONFIG[cmd_tok]
                nodes.append(self.parse_command(obj_name, config))
            else:
                self.error(f"Unknown command '{cmd_tok}' on object '{obj_name}'")
            return

        if tok in TOKEN_TO_CONFIG:
            # Global command: `world(...)`, `show(...)`, `repeat(...) { }`
            config = TOKEN_TO_CONFIG[tok]
            nodes.append(self.parse_command(config.get("default_obj", "global"), config))
            return

        self.error(f"Unexpected token '{tok}'")

    # --- Public API ---

    def parse(self):
        nodes = []
        while self.curr_token[0] != TOKEN_EOF:
            self._parse_statement(nodes)
        return nodes
