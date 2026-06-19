class VirtualMachine:
    def __init__(self, simulator):
        self.simulator = simulator
        self.objects = {}
    
    def error(self, msg):
        raise SyntaxError(f"VM error: {msg}")
    
    def run(self, bytecode):
        for bytecode in bytecode:
            action, id, args = bytecode
            match   action:
                case 1:
                    self.objects[id]['x'] += args[0]
                    self.simulator.move_obj(id, self.objects[id]['x'], self.objects[id]['y'])
                case 2:
                    self.objects[id]['y'] += args[0]
                    self.simulator.move_obj(id, self.objects[id]['x'], self.objects[id]['y'])   
                case 3:
                    self.objects[id] = {'x': args[0], 'y': args[1]}
                    self.simulator.spawn_obj(id, args[0], args[1]) 
                case 4:
                    print("world created")
                case 5:
                    self.simulator.result()