# define tokens
TOKEN_INIT = "INIT"
TOKEN_MOVX = "MOVX"
TOKEN_MOVY = "MOVY"
TOKEN_WORLD = "WORLD"

TOKEN_NUMBER = "NUMBER"
TOKEN_VARIABLE = "VARIABLE"

TOKEN_LPAREN = "LPAREN"
TOKEN_RPAREN = "RPAREN"
TOKEN_DOT = "DOT"
TOKEN_COMMA = "COMMA"
TOKEN_EQ = "="
TOKEN_EOF = "EOF"

# dictionaries
keywords = {
    "world": TOKEN_WORLD,
    "init": TOKEN_INIT,
    "movX": TOKEN_MOVX,
    "movY": TOKEN_MOVY,
}
single_char_tokens = {
    "(": TOKEN_LPAREN,
    ")": TOKEN_RPAREN,
    ".": TOKEN_DOT,
    ",": TOKEN_COMMA,
    "=": TOKEN_EQ,
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
        self.pos +=1
        if self.pos< len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None
    
    def number(self):
        result=""
        while self.current_char and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def getObjectName(self):
        result = ""
        while self.current_char and (self.current_char.isalpha() or self.current_char.isdigit()):
            result += self.current_char
            self.advance()
        if self.current_char == ".":
            return result
        return None
    
    def get_next_token(self):
        while self.current_char:
            if self.current_char.isspace():
                self.advance()
                continue

            if self.current_char.isdigit():
                return (TOKEN_NUMBER, self.number())

            for word in keywords:
                if self.text[self.pos: self.pos+len(word)] == word:
                    self.pos += len(word)
                    self.current_char = self.text[self.pos]
                    return (keywords[word], word)
            
            for char in single_char_tokens:
                if self.current_char == char:
                    self.advance()  
                    return (single_char_tokens[char], char)
            
            objName = self.getObjectName()
            if objName:
                return (TOKEN_VARIABLE , objName)
            
            self.error("Invalid character")
            return
         
            
        return (TOKEN_EOF, None)

