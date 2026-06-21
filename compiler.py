from registry import COMMANDS

OPCODES = {k: v["opcode"] for k, v in COMMANDS.items()}

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
    
    def compile(self, nodes):
        bytecode = []

        for node in nodes:
            if node.action == "skip":
                continue
            action = OPCODES[node.action]
            id = self.get_obj_id(node.name)
            idToName[id] = node.name
            args = node.args
            bytecode.append((action, id, args))
        return bytecode
            
