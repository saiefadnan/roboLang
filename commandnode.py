class CommandNode:
    def __init__(self, name, action, args):
        self.name = name
        self.action = action
        self.args = args
    def __repr__(self):
        return f"CommandNode({self.name}, {self.action}, {self.args})"