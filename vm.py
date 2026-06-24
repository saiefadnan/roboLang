from registry import COMMANDS, OPCODE_TO_CMD
from compiler import idToName

class VirtualMachine:
    def __init__(self, simulator):
        self.simulator = simulator
        self.last_result = None
    
    def error(self, msg):
        raise SystemError(f"VM error: {msg}")
        
    
    def run(self, bytecode, variables = {}, objects = {}):
        
        for cmd in bytecode:
            opcode, obj_id, args, bytecodes = cmd
            
            if len(bytecodes):
                count = self.resolve_variable(args[0], variables) 
                while count>0:
                    self.run(bytecodes, variables, objects)
                    count-=1
                    self.set_variable(args[0], variables, count)
                continue

            cmd_name = OPCODE_TO_CMD.get(opcode)
            if not cmd_name:
                self.error(f"Unknown opcode {opcode}")
            
            # --- CORE VM OPS ---
            if cmd_name == "STORE":
                variables[obj_id] = self.last_result
                continue
            elif cmd_name == "LOAD_VAL":
                self.last_result = args[0]
                continue
            
            config = COMMANDS.get(cmd_name)
            if not config:
                self.error(f"Config not found for {cmd_name}")
                
            handler_name = config["handler"]
            
            # --- GENERIC STATE MANAGEMENT ---
            init_keys = config.get("state_init")
            if init_keys:
                objects[obj_id] = {}
                for i, key in enumerate(init_keys):
                    if i < len(args):
                        objects[obj_id][key] = args[i]
            
            update_rules = config.get("state_update")
            if update_rules:
                if obj_id not in objects:
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
                            objects[obj_id][state_key] += val
                        elif op == "set":
                            objects[obj_id][state_key] = val

            # --- DYNAMIC DISPATCH ---
            if hasattr(self.simulator, handler_name):
                handler = getattr(self.simulator, handler_name)
                # Resolve arguments
                resolved_args = []
                for val in args:
                    if isinstance(val, dict):
                        resolved_args.append(self.resolve_variable(val, variables))
                    else:
                        resolved_args.append(val)
                if(handler_name=="repeat"):
                    print(handler_name)
                if config.get("type") == "object":
                    self.last_result = handler(obj_id, *resolved_args)
                else:
                    self.last_result = handler(*resolved_args)
            else:
                self.error(f"Simulator missing required handler '{handler_name}' for {cmd_name}")


    def resolve_variable(self, arg, variables):
        var_id = self.get_variable_id(arg, variables)
        value = variables[var_id]
        if arg.get("type") == "variable_prop":
            prop = arg["prop"]
            if hasattr(value, prop):
                return getattr(value, prop)
            elif isinstance(value, dict) and prop in value:
                return value[prop]
            else:
                self.error(f"Property '{prop}' not found on variable '{arg['name']}'")
        return value

    def set_variable(self, arg, variables, value):
        var_id = self.get_variable_id(arg, variables)
        variables[var_id] = value
    
    def get_variable_id(self, arg, variables):
        var_id = arg["id"]
        if var_id not in variables:
            self.error(f"Variable with ID {var_id} ({arg['name']}) not found")
        return var_id