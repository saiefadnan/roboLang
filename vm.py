from registry import COMMANDS, OPCODE_TO_CMD

class VirtualMachine:
    def __init__(self, simulator):
        self.simulator = simulator
        self.objects = {}
    
    def error(self, msg):
        raise SystemError(f"VM error: {msg}")
    
    def run(self, bytecode):
        for cmd in bytecode:
            opcode, obj_id, args = cmd
            cmd_name = OPCODE_TO_CMD.get(opcode)
            if not cmd_name:
                self.error(f"Unknown opcode {opcode}")
            
            config = COMMANDS[cmd_name]
            handler_name = config["handler"]
            
            # --- GENERIC STATE MANAGEMENT ---
            # Initializing state based on state_init keys
            init_keys = config.get("state_init")
            if init_keys:
                self.objects[obj_id] = {}
                for i, key in enumerate(init_keys):
                    if i < len(args):
                        self.objects[obj_id][key] = args[i]
            
            # Updating state based on state_update rules
            update_rules = config.get("state_update")
            if update_rules:
                if obj_id not in self.objects:
                    self.error(f"Object {obj_id} not initialized")
                
                for state_key, rule in update_rules.items():
                    arg_idx = rule["arg_idx"]
                    op = rule["op"]
                    if arg_idx < len(args):
                        val = args[arg_idx]
                        if op == "add":
                            self.objects[obj_id][state_key] += val
                        elif op == "set":
                            self.objects[obj_id][state_key] = val
                        else:
                            self.error(f"Unknown state operation '{op}'")

            # --- DYNAMIC DISPATCH ---
            if hasattr(self.simulator, handler_name):
                handler = getattr(self.simulator, handler_name)
                if config.get("type") == "object":
                    handler(obj_id, *args)
                else:
                    handler(*args)
            else:
                self.error(f"Simulator missing required handler '{handler_name}' for {cmd_name}")