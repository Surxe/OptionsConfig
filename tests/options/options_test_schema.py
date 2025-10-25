"""
Test schema for Options class tests
"""

from pathlib import Path
from typing import Literal

# Schema without dependencies for basic tests
OPTIONS_SCHEMA_BASIC = {
    # String option
    "PROJECT_NAME": {
        "env": "PROJECT_NAME",
        "arg": "--project-name",
        "type": str,
        "default": "MyProject",
        "section": "Project",
        "help": "Name of the project"
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
    
    # Log level option (Literal type)
    "LOG_LEVEL": {
        "env": "LOG_LEVEL",
        "arg": "--log-level",
        "type": Literal["DEBUG", "INFO", "WARNING", "ERROR"],
        "default": "INFO",
        "section": "Logging",
        "help": "Logging level"
    },
    
    # Sensitive option
    "API_KEY": {
        "env": "API_KEY",
        "arg": "--api-key",
        "type": str,
        "default": None,
        "section": "Security",
        "help": "API key for authentication",
        "sensitive": True
    },
    
    # Integer option
    "MAX_RETRIES": {
        "env": "MAX_RETRIES",
        "arg": "--max-retries",
        "type": int,
        "default": 3,
        "section": "Network",
        "help": "Maximum number of retry attempts"
    }
}

# Schema with dependencies for dependency validation tests
OPTIONS_SCHEMA_WITH_DEPS = {
    # Root option that others depend on
    "ENABLE_PROCESSING": {
        "env": "ENABLE_PROCESSING",
        "arg": "--enable-processing",
        "type": bool,
        "default": False,
        "section": "General",
        "help": "Enable data processing"
    },
    
    # Dependent option - required when ENABLE_PROCESSING is True
    "OUTPUT_FILE": {
        "env": "OUTPUT_FILE",
        "arg": "--output-file",
        "type": Path,
        "default": None,
        "section": "Output",
        "help": "Output file path (required when processing is enabled)",
        "depends_on": ["ENABLE_PROCESSING"]
    },
    
    # Non-dependent option
    "PROJECT_NAME": {
        "env": "PROJECT_NAME",
        "arg": "--project-name",
        "type": str,
        "default": "MyProject",
        "section": "Project",
        "help": "Name of the project"
    }
}

# Default export for backwards compatibility
OPTIONS_SCHEMA = OPTIONS_SCHEMA_BASIC
