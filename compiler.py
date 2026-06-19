OPCODES = {
    "movX": 1,
    "movY": 2,
    "init": 3,
    "create": 4
}

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
            action = OPCODES[node.action]
            id = self.get_obj_id(node.name)
            idToName[id] = node.name
            args = node.args
            bytecode.append((action, id, args))
        return bytecode
            
