from registry import COMMANDS, CORE_OPCODES
from commandnode import CommandNode

# Flat opcode lookup: command_name -> opcode integer
OPCODES = {k: v["opcode"] for k, v in COMMANDS.items()}
OPCODES.update(CORE_OPCODES)

# Human-readable name lookup (populated at compile time)
idToName = {}


class Compiler:
    def __init__(self):
        self.symbols = {}   # name -> unique int ID
        self.next_id = 0

    def get_obj_id(self, name):
        if name not in self.symbols:
            self.symbols[name] = self.next_id
            idToName[self.next_id] = name
            self.next_id += 1
        return self.symbols[name]

    def resolve_arg(self, arg):
        """Resolve a single argument, embedding the variable's ID for the VM."""
        if isinstance(arg, dict) and arg.get("type") in ("variable", "variable_prop"):
            new_arg = arg.copy()
            new_arg["id"] = self.get_obj_id(arg["name"])
            return new_arg
        return arg

    def compile_node(self, node):
        if node.action == "skip":
            return []

        # --- Variable assignment ---
        if node.action == "assign":
            bytecode = []
            rhs = node.args[0]
            if isinstance(rhs, CommandNode):
                bytecode.extend(self.compile_node(rhs))
            else:
                # Load a literal value into last_result
                bytecode.append((OPCODES["LOAD_VAL"], 0, [rhs], []))

            var_id = self.get_obj_id(node.name)
            bytecode.append((OPCODES["STORE"], var_id, [], []))
            return bytecode

        # --- Normal command ---
        opcode   = OPCODES[node.action]
        obj_id   = self.get_obj_id(node.name)
        resolved = [self.resolve_arg(a) for a in node.args]

        # Recursively compile nested block (e.g. repeat body)
        body_bytecode = self.compile(node.nodes) if node.nodes else []

        return [(opcode, obj_id, resolved, body_bytecode)]

    def compile(self, nodes):
        result = []
        for node in nodes:
            result.extend(self.compile_node(node))
        return result
