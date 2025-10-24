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
        "type": str,
        "default": None,
        "section": "Features",
        "depends_on": ["ENABLE_FEATURE"],
        "help": "Path to the feature configuration file"
    },
}