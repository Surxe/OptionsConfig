from pathlib import Path

OPTIONS_SCHEMA = {
    "ENABLE_FEATURE": {
        "env": "ENABLE_FEATURE",
        "arg": "--enable-feature",
        "type": bool,
        "default": True,
        "section": "Features",
        "help": "Enable the special feature"
    },
    "FEATURE_PATH": {
        "env": "FEATURE_PATH",
        "arg": "--feature-path",
        "type": Path,
        "default": None,
        "section": "Features",
        "depends_on": ["ENABLE_FEATURE"],
        "help": "Path to the feature configuration file",
        "example": Path("C:/example/path/to/feature.py"),
        "links": {
            "Documentation": "https://example.com/docs/feature-path"
        }
    },
    "LOG_LEVEL": {
        "env": "LOG_LEVEL",
        "arg": "--log-level",
        "type": str,
        "default": "INFO",
        "section": "Logging",
        "help": "Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
        "example": "DEBUG"
    },
}
