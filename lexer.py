# define tokens
TOKEN_INIT = "INIT"
TOKEN_MOVX = "MOVX"
TOKEN_MOVY = "MOVY"
TOKEN_RESULT = "RESULT"
TOKEN_WORLD = "WORLD"

TOKEN_NUMBER = "NUMBER"
TOKEN_VARIABLE = "VARIABLE"

TOKEN_LPAREN = "LPAREN"
TOKEN_RPAREN = "RPAREN"
TOKEN_DOT = "DOT"
TOKEN_COMMA = "COMMA"
TOKEN_EQ = "="
TOKEN_COMMENT = "COMMENT"
TOKEN_NEWLINE = "NEWLINE"
TOKEN_EOF = "EOF"

# dictionaries
keywords = {
    "world": TOKEN_WORLD,
    "init": TOKEN_INIT,
    "movX": TOKEN_MOVX,
    "movY": TOKEN_MOVY,
    "result": TOKEN_RESULT,
}
single_char_tokens = {
    "(": TOKEN_LPAREN,
    ")": TOKEN_RPAREN,
    ".": TOKEN_DOT,
    ",": TOKEN_COMMA,
    "=": TOKEN_EQ,
    "#": TOKEN_COMMENT
}


# breaks source code into meaningful tokens
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = text[self.pos]

    def error(self, msg="Invalid character"):
        raise SystemError(f"Lexer error at position {self.pos}: {msg} ('{self.current_char}')")

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def _id(self):
        result = ""
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        token_type = keywords.get(result, TOKEN_VARIABLE)
        return (token_type, result)

    def number(self):
        result = ""
        while self.current_char and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return (TOKEN_NUMBER, int(result))

    def get_next_token(self):
        while self.current_char:
            if self.current_char == "\n":
                self.advance()
                return (TOKEN_NEWLINE, "\n")

            if self.current_char.isspace():
                self.advance()
                continue

            if self.current_char.isdigit():
                return self.number()

            if self.current_char.isalpha() or self.current_char == '_':
                return self._id()

            if self.current_char in single_char_tokens:
                char = self.current_char
                token_type = single_char_tokens[char]
                self.advance()
                return (token_type, char)

            self.error()

        return (TOKEN_EOF, None)
         
            
        return (TOKEN_EOF, None)

