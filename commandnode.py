class CommandNode:
    def __init__(self, name, action, args, nodes=None):
        self.name = name
        self.action = action
        self.args = args
        self.nodes = nodes if nodes is not None else []

    def __repr__(self):
        return f"CommandNode({self.name}, {self.action}, {self.args}, {self.nodes})"