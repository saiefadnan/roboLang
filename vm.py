from registry import COMMANDS, OPCODE_TO_CMD
from compiler import idToName


class VirtualMachine:
    def __init__(self, simulator):
        self.simulator = simulator
        self.last_result = None

    def error(self, msg):
        raise SystemError(f"VM error: {msg}")

    # ------------------------------------------------------------------ #
    #  Main execution loop                                                 #
    # ------------------------------------------------------------------ #

    def run(self, bytecode, variables=None, objects=None):
        # Allow nested calls (repeat body) to share the same state dicts
        if variables is None:
            variables = {}
        if objects is None:
            objects = {}

        for cmd in bytecode:
            opcode, obj_id, args, body = cmd

            # ── Control-flow: commands that carry a nested body ──────────
            if body:
                self._execute_block_cmd(opcode, obj_id, args, body, variables, objects)
                continue

            # ── Opcode lookup ────────────────────────────────────────────
            cmd_name = OPCODE_TO_CMD.get(opcode)
            if cmd_name is None:
                self.error(f"Unknown opcode {opcode}")

            # ── Core VM ops ──────────────────────────────────────────────
            if cmd_name == "STORE":
                variables[obj_id] = self.last_result
                continue

            if cmd_name == "LOAD_VAL":
                self.last_result = args[0]
                continue

            # ── Regular command ──────────────────────────────────────────
            self._execute_command(cmd_name, obj_id, args, variables, objects)

    # ------------------------------------------------------------------ #
    #  Block command execution (e.g. repeat)                              #
    # ------------------------------------------------------------------ #

    def _execute_block_cmd(self, opcode, obj_id, args, body, variables, objects):
        cmd_name = OPCODE_TO_CMD.get(opcode)
        if cmd_name is None:
            self.error(f"Unknown opcode {opcode} in block command")

        config = COMMANDS.get(cmd_name)
        if config is None:
            self.error(f"Config not found for block command '{cmd_name}'")

        # Resolve the iteration count (can be a variable or a literal)
        count = self._resolve_arg(args[0], variables) if args else 0
        if not isinstance(count, int):
            self.error(f"'repeat' count must be an integer, got {type(count).__name__}")

        for _ in range(count):
            self.run(body, variables, objects)

    # ------------------------------------------------------------------ #
    #  Regular command execution                                           #
    # ------------------------------------------------------------------ #

    def _execute_command(self, cmd_name, obj_id, args, variables, objects):
        config = COMMANDS.get(cmd_name)
        if config is None:
            self.error(f"Config not found for '{cmd_name}'")

        handler_name = config["handler"]

        # ── State initialisation ─────────────────────────────────────────
        init_keys = config.get("state_init")
        if init_keys:
            objects[obj_id] = {
                key: args[i]
                for i, key in enumerate(init_keys)
                if i < len(args)
            }

        # ── State update ─────────────────────────────────────────────────
        update_rules = config.get("state_update")
        if update_rules:
            if obj_id not in objects:
                self.error(f"Object '{idToName.get(obj_id, obj_id)}' used before init")
            for state_key, rule in update_rules.items():
                idx = rule["arg_idx"]
                op  = rule["op"]
                if idx < len(args):
                    val = self._resolve_arg(args[idx], variables)
                    if op == "add":
                        objects[obj_id][state_key] += val
                    elif op == "set":
                        objects[obj_id][state_key] = val
                    # More ops can be added here (mul, div …)

        # ── Dispatch to simulator ────────────────────────────────────────
        if not hasattr(self.simulator, handler_name):
            self.error(f"Simulator is missing handler '{handler_name}' for '{cmd_name}'")

        handler = getattr(self.simulator, handler_name)
        resolved = [self._resolve_arg(a, variables) for a in args]

        if config.get("type") == "object":
            self.last_result = handler(obj_id, *resolved)
        else:
            self.last_result = handler(*resolved)

    # ------------------------------------------------------------------ #
    #  Variable resolution                                                 #
    # ------------------------------------------------------------------ #

    def _resolve_arg(self, arg, variables):
        print(f"assddddddddddddddd {arg}")
        """Return the concrete value for `arg` (literal or variable lookup)."""
        if not isinstance(arg, dict):
            return arg

        var_id = arg.get("id")
        if var_id is None:
            self.error(f"Unresolved variable reference (no id): {arg}")
        if var_id not in variables:
            name = arg.get("name", var_id)
            self.error(f"Variable '{name}' used before assignment")

        value = variables[var_id]

        if arg.get("type") == "variable_prop":
            prop = arg["prop"]
            if hasattr(value, prop):
                return getattr(value, prop)
            if isinstance(value, dict) and prop in value:
                return value[prop]
            name = arg.get("name", var_id)
            self.error(f"Property '{prop}' not found on variable '{name}'")

        return value