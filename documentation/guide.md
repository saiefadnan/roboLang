# roboLang — Complete Execution Guide (Build-It-From-Scratch Version)

### Goal

Build a robotics-focused programming language step-by-step with working outputs at every phase.

---

# 🧠 Core Rule (DO NOT IGNORE)

Every phase must produce a **working program**, not just theory.

If a phase doesn’t run code → you’re doing it wrong.

---

# 🏗️ Final System You Are Building

```text
roboLang code
    ↓
Lexer (tokens)
    ↓
Parser (AST)
    ↓
Interpreter (execution)
    ↓
Simulator (visual robot world)
    ↓
Extended runtime (sensors + AI)
```

---

# 📁 PROJECT SETUP (Do this FIRST)

## Step 0.1 — Create project structure

```bash
robolang/
│
├── main.py
├── lexer.py
├── parser.py
├── ast.py
├── interpreter.py
├── simulator.py
├── robot.py
└── tests/
```

---

## Step 0.2 — Define minimal language

Start ONLY with this:

```robot
movX(10)
movY(90)
```

No variables. No if. No loops.

---

# 🔤 PHASE 1 — LEXER (MAKE CODE → TOKENS)

## 🎯 Goal

Convert raw text into structured tokens.

---

## Step 1.1 — Define token types (lexer.py)

```python
TOKEN_movX = "movX"
TOKEN_movY = "movY"
TOKEN_NUMBER = "NUMBER"
TOKEN_LPAREN = "("
TOKEN_RPAREN = ")"
TOKEN_EOF = "EOF"
```

---

## Step 1.2 — Write lexer class

```python
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = text[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None
```

---

## Step 1.3 — Extract numbers

```python
def number(self):
    result = ""
    while self.current_char and self.current_char.isdigit():
        result += self.current_char
        self.advance()
    return int(result)
```

---

## Step 1.4 — Generate tokens

```python
def get_next_token(self):
    while self.current_char:
        if self.current_char.isspace():
            self.advance()
            continue

        if self.current_char.isdigit():
            return ("NUMBER", self.number())

        if self.text[self.pos:self.pos+4] == "movX":
            self.pos += 4
            self.current_char = self.text[self.pos]
            return ("movX", "movX")

        if self.text[self.pos:self.pos+4] == "movY":
            self.pos += 4
            self.current_char = self.text[self.pos]
            return ("movY", "movY")

        if self.current_char == "(":
            self.advance()
            return ("LPAREN", "(")

        if self.current_char == ")":
            self.advance()
            return ("RPAREN", ")")

    return ("EOF", None)
```

---

## ✅ PHASE 1 TEST (VERY IMPORTANT)

### main.py

```python
from lexer import Lexer

code = "movX(10) movY(90)"
lexer = Lexer(code)

token = lexer.get_next_token()
while token[0] != "EOF":
    print(token)
    token = lexer.get_next_token()
```

---

## 🎯 Expected output:

```text
('movX', 'movX')
('LPAREN', '(')
('NUMBER', 10)
('RPAREN', ')')
...
```

---

# 🌳 PHASE 2 — PARSER (TOKENS → AST)

## 🎯 Goal

Convert tokens into structured tree.

---

## Step 2.1 — Define AST (ast.py)

```python
class movXNode:
    def __init__(self, value):
        self.value = value

class movYNode:
    def __init__(self, value):
        self.value = value
```

---

## Step 2.2 — Parser skeleton

```python
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = lexer.get_next_token()
```

---

## Step 2.3 — Parse movX()

```python
def parse_movX(self):
    self.eat("movX")
    self.eat("LPAREN")
    value = self.current_token[1]
    self.eat("NUMBER")
    self.eat("RPAREN")
    return movXNode(value)
```

---

## Step 2.4 — Parse full program

```python
def parse(self):
    nodes = []

    while self.current_token[0] != "EOF":
        if self.current_token[0] == "movX":
            nodes.append(self.parse_movX())

        elif self.current_token[0] == "movY":
            nodes.append(self.parse_movY())

    return nodes
```

---

## ✅ PHASE 2 TEST

```python
parser = Parser(lexer)
ast = parser.parse()

print(ast)
```

---

## 🎯 Expected output:

```text
[movXNode(10), movYNode(90)]
```

---

# ⚙️ PHASE 3 — INTERPRETER (AST → EXECUTION)

## 🎯 Goal

Make robot actually “do things”.

---

## Step 3.1 — Fake robot (robot.py)

```python
class Robot:
    def movX(self, value):
        print(f"Moving {value}")

    def movY(self, value):
        print(f"movYing {value}")
```

---

## Step 3.2 — Interpreter

```python
class Interpreter:
    def __init__(self, robot):
        self.robot = robot

    def visit(self, node):
        if isinstance(node, movXNode):
            self.robot.movX(node.value)

        elif isinstance(node, movYNode):
            self.robot.movY(node.value)
```

---

## Step 3.3 — Run program

```python
for node in ast:
    interpreter.visit(node)
```

---

## 🎯 Output:

```text
Moving 10
movYing 90
```

---

# 🌍 PHASE 4 — SIMULATOR (REAL BREAKTHROUGH)

## 🎯 Goal

Replace print() with a visual world.

---

## Step 4.1 — Create grid world

```python
class World:
    def __init__(self):
        self.x = 0
        self.y = 0
```

---

## Step 4.2 — Replace robot logic

```python
class Robot:
    def movX(self, value):
        self.x += value
        print(f"Robot at {self.x}, {self.y}")
```

---

## Step 4.3 — Add visualization (optional)

Use:

- matplotlib OR
- pygame OR
- simple terminal grid

---

## 🎯 Result:

You SEE robot moving.

---

# 🧠 PHASE 5 — LANGUAGE EXPANSION

Add:

## IF condition

```robot
if detect("wall") {
    movY(90)
}
```

## Variables

```robot
let x = 10
```

---

# 👁️ PHASE 6 — SENSOR SYSTEM

## Replace fake logic with:

```python
def distance():
    return simulated_distance()
```

---

# ⚡ PHASE 7 — VM (OPTIONAL OPTIMIZATION)

Convert AST → bytecode:

```text
movX 10
movY 90
```

Run faster execution engine.

---

# 🚀 PHASE 8 — BACKEND SYSTEM

Add abstraction:

```text
Interpreter
   ↓
Robot API
   ↓
[Simulator | Hardware | AI]
```

---

# 🧪 PHASE 9 — HARDWARE (OPTIONAL FINAL)

Send commands:

```python
serial.write("movX 10")
```

---

# 📊 HOW YOU TRACK PROGRESS

Every phase MUST give:

| Phase       | Output             |
| ----------- | ------------------ |
| Lexer       | tokens printed     |
| Parser      | AST printed        |
| Interpreter | text execution     |
| Simulator   | visible movXment   |
| Sensors     | fake data working  |
| VM          | bytecode execution |

---

# ❌ RULES TO NOT FAIL

- Don’t jump to AI early
- Don’t skip lexer/parser
- Don’t mix phases
- Don’t overdesign syntax
- Always build working output

---

# 🎯 FINAL RESULT

You will end up with:

```robot
movX(10)
movY(90)
scan()
follow("person")
```

and a system that:

- parses it
- understands it
- executes it
- simulates it
- (optionally) runs on real robots

---

# 🧠 REAL PURPOSE

You are not building a language.

You are building a full stack:

> Language + Compiler + Runtime + Simulation Engine
