"""
Test schema for ArgumentWriter tests
"""

from pathlib import Path
from typing import Literal

OPTIONS_SCHEMA = {
    # Boolean option
    "VERBOSE": {
        "env": "VERBOSE",
        "arg": "--verbose",
        "type": bool,
        "default": False,
        "section": "General",
        "help": "Enable verbose output"
    },
    
    # String option
    "OUTPUT_FILE": {
        "env": "OUTPUT_FILE",
        "arg": "--output-file",
        "type": str,
        "default": "output.txt",
        "section": "Output",
        "help": "Output file path"
    },
    
    # Integer option
    "MAX_WORKERS": {
        "env": "MAX_WORKERS",
        "arg": "--max-workers",
        "type": int,
        "default": 4,
        "section": "Performance",
        "help": "Maximum number of worker threads"
    },
    
    # Float option
    "THRESHOLD": {
        "env": "THRESHOLD",
        "arg": "--threshold",
        "type": float,
        "default": 0.5,
        "section": "Settings",
        "help": "Threshold value for processing"
    },
    
    # Path option
    "DATA_DIR": {
        "env": "DATA_DIR",
        "arg": "--data-dir",
        "type": Path,
        "default": Path("data"),
        "section": "Paths",
        "help": "Directory for data files"
    },
    
    # Literal (choice) option
    "LOG_LEVEL": {
        "env": "LOG_LEVEL",
        "arg": "--log-level",
        "type": Literal["DEBUG", "INFO", "WARNING", "ERROR"],
        "default": "INFO",
        "section": "Logging",
        "help": "Logging level"
    },
    
    # Option with dependency
    "CONFIG_FILE": {
        "env": "CONFIG_FILE",
        "arg": "--config-file",
        "type": Path,
        "default": None,
        "section": "Configuration",
        "help": "Configuration file path",
        "depends_on": ["VERBOSE"]
    }
}
