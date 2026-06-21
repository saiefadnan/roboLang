from registry import KEYWORD_TO_TOKEN, SYMBOLS

# define tokens
TOKEN_NUMBER = "NUMBER"
TOKEN_STRING = "STRING"
TOKEN_VARIABLE = "VARIABLE"
TOKEN_NEWLINE = "NEWLINE"
TOKEN_EOF = "EOF"

# Dynamic keywords from registry
keywords = KEYWORD_TO_TOKEN

# Dynamic symbols from registry
single_char_tokens = SYMBOLS

# Add symbols to globals so they can be referenced as TOKEN_LPAREN etc.
for sym, token_name in SYMBOLS.items():
    globals()[f"TOKEN_{token_name}"] = token_name

# Add other tokens from registry configs if needed
from registry import TOKEN_TO_CONFIG
for token_name in TOKEN_TO_CONFIG:
    if f"TOKEN_{token_name}" not in globals():
        globals()[f"TOKEN_{token_name}"] = token_name


# breaks source code into meaningful tokens
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = text[self.pos] if text else None

    def error(self, msg="Invalid character"):
        char = self.current_char if self.current_char else "EOF"
        raise SystemError(f"Lexer error at position {self.pos}: {msg} ('{char}')")

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

    def string(self):
        result = ""
        self.advance() # Skip opening quote
        while self.current_char and self.current_char != '"':
            result += self.current_char
            self.advance()
        if self.current_char == '"':
            self.advance() # Skip closing quote
        return (TOKEN_STRING, result)

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

            if self.current_char == '"':
                return self.string()

            if self.current_char.isalpha() or self.current_char == '_':
                return self._id()

            if self.current_char in single_char_tokens:
                char = self.current_char
                token_type = single_char_tokens[char]
                self.advance()
                return (token_type, char)

            self.error()

        return (TOKEN_EOF, None)
