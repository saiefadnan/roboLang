from registry import COMMANDS, OPCODE_TO_CMD
from compiler import idToName

class VirtualMachine:
    def __init__(self, simulator):
        self.simulator = simulator
        self.objects = {}
        self.variables = {}
        self.last_result = None
    
    def error(self, msg):
        raise SystemError(f"VM error: {msg}")
    
    def run(self, bytecode):
        for cmd in bytecode:
            opcode, obj_id, args = cmd
            cmd_name = OPCODE_TO_CMD.get(opcode)
            
            if not cmd_name:
                self.error(f"Unknown opcode {opcode}")
            
            # --- CORE VM OPS ---
            if cmd_name == "STORE":
                self.variables[obj_id] = self.last_result
                continue
            # elif cmd_name == "LOAD_VAL":
            #     self.last_result = args[0]
            #     continue
            
            config = COMMANDS.get(cmd_name)
            if not config:
                self.error(f"Config not found for {cmd_name}")
                
            handler_name = config["handler"]
            
            # --- GENERIC STATE MANAGEMENT ---
            init_keys = config.get("state_init")
            if init_keys:
                self.objects[obj_id] = {}
                for i, key in enumerate(init_keys):
                    if i < len(args):
                        self.objects[obj_id][key] = args[i]
            
            update_rules = config.get("state_update")
            if update_rules:
                if obj_id not in self.objects:
                    self.error(f"Object {obj_id} not initialized")
                for state_key, rule in update_rules.items():
                    arg_idx = rule["arg_idx"]
                    op = rule["op"]
                    if arg_idx < len(args):
                        val = args[arg_idx]
                        if isinstance(val, dict):
                            val = self.resolve_variable(val)
                        # TODO: Add more operations
                        if op == "add":
                            self.objects[obj_id][state_key] += val
                        elif op == "set":
                            self.objects[obj_id][state_key] = val

            # --- DYNAMIC DISPATCH ---
            if hasattr(self.simulator, handler_name):
                handler = getattr(self.simulator, handler_name)
                
                # Resolve arguments
                resolved_args = []
                for val in args:
                    if isinstance(val, dict):
                        resolved_args.append(self.resolve_variable(val))
                    else:
                        resolved_args.append(val)
                
                if config.get("type") == "object":
                    self.last_result = handler(obj_id, *resolved_args)
                else:
                    self.last_result = handler(*resolved_args)
            else:
                self.error(f"Simulator missing required handler '{handler_name}' for {cmd_name}")

    def resolve_variable(self, arg):
        var_id = arg["id"]
        if var_id not in self.variables:
            self.error(f"Variable with ID {var_id} ({arg['name']}) not found")
        
        value = self.variables[var_id]
        if arg.get("type") == "variable_prop":
            prop = arg["prop"]
            if hasattr(value, prop):
                return getattr(value, prop)
            elif isinstance(value, dict) and prop in value:
                return value[prop]
            else:
                self.error(f"Property '{prop}' not found on variable '{arg['name']}'")
        return value