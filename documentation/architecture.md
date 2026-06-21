# roboLang Architecture Guide

roboLang is a bytecode-based language designed for robotic simulation. The architecture is 100% data-driven, meaning you can extend the language by only modifying configuration and implementation files.

## High-Level Pipeline
1. **Lexer**: Tokenizes source code (supports keywords, numbers, strings, comments).
2. **Parser**: Generates a Custom Node Tree (AST) while validating types and argument counts.
3. **Compiler**: Translates AST nodes into 3-tuple bytecode `(opcode, id, args)`.
4. **VM**: Executes bytecode, manages robot state, and dispatches commands to the Simulator.
5. **Simulator**: Handles the actual visualization (Turtle graphics).

---

## 🔌 The "Plug-and-Play" System
Adding a new rule to roboLang is as simple as updating two files.

### Step 1: Register in `registry.py`
Add your command to the `COMMANDS` dictionary.

```python
"teleport": {
    "token": "TELEPORT",       # The keyword used in the language
    "opcode": 10,              # A unique integer for the VM
    "arg_types": ["int", "int"], # Arguments to eat (int or str)
    "handler": "teleport",     # Method name in simulator.py
    "type": "object",          # "object" (r1.cmd) or "global" (cmd)
    "state_update": {          # (Optional) Update VM's internal state
        "x": {"arg_idx": 0, "op": "set"},
        "y": {"arg_idx": 1, "op": "set"}
    }
}
```

### Step 2: Implement in `simulator.py`
Add the handler method to the `Simulator` class.

```python
def teleport(self, id, x, y):
    name = idToName[id]
    self.objs[id]["x"] = x
    self.objs[id]["y"] = y
    self.objs[id]["obj"].goto(x, y)
    print(f"Visualization: {name} teleported to ({x}, {y})")
```

---

## 🛠️ Components Detail

### Registry (`registry.py`)
The "Brain" of the language. It controls keywords, opcodes, validation rules, and state transformation logic.
- **`state_init`**: Use this for the `init` command to bootstrap robot coordinates.
- **`state_update`**: Use this to keep the VM in sync with coordinates for collision detection.

### Virtual Machine (`vm.py`)
A generic executor. It has **no hardcoded knowledge** of specific commands like `movX`. It relies entirely on the mappings in the registry to update state and dispatch calls.

### Parser (`parser.py`)
A data-driven syntax checker. It uses the `arg_types` metadata to strictly enforce what kind of data (integers or strings) can be passed to each command.

### Lexer (`lexer.py`)
Automatically picks up new keywords from the registry and supports full string literal parsing (`"..."`).

---

## 🚀 Adding a Global Command
If you want to add a command like `clear()`, set `"type": "global"` in the registry. The VM will call `simulator.clear()` directly with whatever arguments you provide.
