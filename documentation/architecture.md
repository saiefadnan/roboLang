# roboLang Architecture Guide

roboLang is a bytecode-based language designed for robotic simulation. The architecture is 100% data-driven, meaning you can extend the language by only modifying configuration and implementation files.

## High-Level Pipeline
1. **Lexer**: Tokenizes source code using dynamic symbols and keywords from the registry.
2. **Parser**: Generates a Custom Node Tree (AST) while validating types, identifying variable assignments, and property access.
3. **Compiler**: Translates AST nodes into bytecode and maps variable names to unique IDs.
4. **VM**: Executes bytecode, manages robot state, handles variable storage, and resolves property access at runtime.
5. **Simulator**: Handles the actual visualization (Turtle graphics) and returns structured results.

---

## 🔌 The "Plug-and-Play" System
Adding a new rule to roboLang is as simple as updating two files.

### Step 1: Register in `registry.py`
Add your command, core keyword, or symbol.

```python
# To add a command
"teleport": {
    "token": "TELEPORT",
    "opcode": 10,
    "arg_types": ["int", "int"],
    "handler": "teleport",
    "type": "object",
    "state_update": {"x": {"arg_idx": 0, "op": "set"}, "y": {"arg_idx": 1, "op": "set"}}
}

# To change a symbol
SYMBOLS = {
    ...
    "=": "EQ", # You can change "=" to "is" if you want!
}
```

### Step 2: Implement in `simulator.py`
Add the handler method to the `Simulator` class.

```python
def teleport(self, id, x, y):
    ...
    return PosResult(x, y) # Return a result if you want to store it in a variable
```

---

## 📦 Variable System
roboLang supports variable declarations with `var` and property access with `.`.
The VM stores results of commands in a specialized variable memory. When a command argument is a variable property (e.g., `hello.x`), the VM resolves it using `resolve_variable` before calling the simulator handler.
