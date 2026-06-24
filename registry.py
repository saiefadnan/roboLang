# roboLang Command Registry

# Command Metadata:
# - opcode: Unique integer for the VM
# - arg_types: List of "int" or "str"
# - handler: Name of the method in Simulator or VM to handle this command
# - type: "object" (call on a robot like r1.movX) or "global" (call like world())
# - state_init: List of state keys to initialize from arguments (e.g., ["x", "y"])
# - state_update: Dictionary mapping state keys to update rules:
#     - arg_idx: Index of the argument in the command
#     - op: "add" (relative) or "set" (absolute)

COMMANDS = {
    "init": {
        "token": "INIT",
        "opcode": 3,
        "arg_types": ["int", "int"],
        "handler": "spawn_obj",
        "type": "object",
        "state_init": ["x", "y"]
    },
    "movX": {
        "token": "MOVX",
        "opcode": 1,
        "arg_types": ["int"],
        "handler": "move_obj_x",
        "type": "object",
        "state_update": {"x": {"arg_idx": 0, "op": "add"}}
    },
    "movY": {
        "token": "MOVY",
        "opcode": 2,
        "arg_types": ["int"],
        "handler": "move_obj_y",
        "type": "object",
        "state_update": {"y": {"arg_idx": 0, "op": "add"}}
    },
    "world": {
        "token": "WORLD",
        "opcode": 4,
        "arg_types": ["int", "int"],
        "handler": "create_world",
        "type": "global"
    },
    "result": {
        "token": "RESULT",
        "opcode": 5,
        "arg_types": [],
        "handler": "result",
        "type": "global"
    },
    "patrol": {
        "token": "PATROL",
        "opcode": 6,
        "arg_types": ["int"],
        "handler": "patrol",
        "type": "object"
    },
    "say": {
        "token": "SAY",
        "opcode": 7,
        "arg_types": ["str"],
        "handler": "say",
        "type": "object"
    },
    "getPos": {
        "token": "GETPOS",
        "opcode": 8,
        "arg_types": [],
        "handler": "get_pos",   
        "type": "object"
    },
    "show": {
        "token": "SHOW",
        "opcode": 9,
        "arg_types": ["any"],
        "handler": "show",
        "type": "global"
    },
    "repeat": {
        "token": "REPEAT",
        "opcode": 10,
        "arg_types": ["int"],
        "handler": "repeat",
        "type": "global",
        "block": True
    }
}

# Internal Opcodes
CORE_OPCODES = {
    "STORE": -10,
    "LOAD": -11,
    "LOAD_VAL": -12
}

CORE_KEYWORDS = {
    "var": "VAR"
}

SYMBOLS = {
    "(": "LPAREN",
    ")": "RPAREN",
    ".": "DOT",
    ",": "COMMA",
    "=": "EQ",
    "#": "COMMENT",
    "{": "LBRACE",
    "}": "RBRACE",
    "+": "PLUS",
    "-": "MINUS",
    "*": "MULTIPLY",
    "/": "DIVIDE"
}


# Calculated Metadata
OPCODE_TO_CMD = {v["opcode"]: k for k, v in COMMANDS.items()}
OPCODE_TO_CMD.update({v: k for k, v in CORE_OPCODES.items()})

# print(OPCODE_TO_CMD)


KEYWORD_TO_TOKEN = {k: v["token"] for k, v in COMMANDS.items()}
KEYWORD_TO_TOKEN.update(CORE_KEYWORDS)
TOKEN_TO_CONFIG = {v["token"]: {"name": k, **v} for k, v in COMMANDS.items()}

# print(TOKEN_TO_CONFIG)