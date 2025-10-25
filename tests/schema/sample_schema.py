from typing import Literal

"""
**should_** - Main action flags (e.g., `should_parse`)
"""

OPTIONS_SCHEMA = {
    "SHOULD_PARSE": {
        "env": "SHOULD_PARSE",
        "arg": "--should-parse",
        "type": bool,
        "default": False,
        "section": "Parse",
        "help": "Whether to parse the game files after downloading."
    },
    "GAME_NAME": {
        "env": "GAME_NAME",
        "arg": "--game-name",
        "type": str,
        "default": "WRFrontiers",
        "section": "Parse",
        "depends_on": ["SHOULD_PARSE"],
        "help": "Name of the game to download."
    },
}