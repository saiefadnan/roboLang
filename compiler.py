from registry import COMMANDS, CORE_OPCODES
from commandnode import CommandNode

OPCODES = {k: v["opcode"] for k, v in COMMANDS.items()}
OPCODES.update(CORE_OPCODES)

idToName = {}

class Compiler:
    def __init__(self):
        self.symbols = {}
        self.next_id = 0

    def get_obj_id(self, name):
        if name not in self.symbols:
            self.symbols[name] = self.next_id
            self.next_id += 1
        return self.symbols[name]
    
    def compile_node(self, node):
        bytecode = []
        if node.action == "skip":
            return []
        
        if node.action == "assign":
            rhs = node.args[0]
            if isinstance(rhs, CommandNode):
                bytecode.extend(self.compile_node(rhs))
            else:
                # Load literal
                bytecode.append((12, 0, [rhs]))
            
            var_id = self.get_obj_id(node.name)
            idToName[var_id] = node.name
            bytecode.append((OPCODES["STORE"], var_id, []))
            return bytecode

        # Normal command
        action = OPCODES[node.action]
        obj_id = self.get_obj_id(node.name)
        idToName[obj_id] = node.name
        
        # Compile/Resolve arguments (map names to IDs for variable access)
        resolved_args = []
        for arg in node.args:
            if isinstance(arg, dict) and arg.get("type") in ["variable", "variable_prop"]:
                new_arg = arg.copy()
                new_arg["id"] = self.get_obj_id(arg["name"])
                resolved_args.append(new_arg)
            else:
                resolved_args.append(arg)
                
        bytecode.append((action, obj_id, resolved_args))
        return bytecode

    def compile(self, nodes):
        full_bytecode = []
        for node in nodes:
            full_bytecode.extend(self.compile_node(node))
        return full_bytecode
