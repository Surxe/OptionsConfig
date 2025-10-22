"""
Options class for managing application configuration
"""

from dotenv import load_dotenv
import os
import sys
from argparse import Namespace
from typing import Literal, get_origin, get_args
from pathlib import Path
from loguru import logger

from .core import get_schema

load_dotenv()


class Options:
    """
    A class to hold options for the application.
    """
    def __init__(self, args: Namespace | None = None, schema: dict | None = None, log_file: str | Path | None = None):
        self.schema = get_schema(schema=schema)
        self.log_file = self._get_log_file(log_file)

        # Initialize all options in the following preference
        # 1. Direct args (if provided)
        # 2. Environment variables (if set)
        # 3. Defaults from OPTIONS_SCHEMA

        # If args is provided, it should be a Namespace from argparse
        if args is not None:
            args_dict = vars(args)
        else:
            args_dict = {}

        # Identify root options (options that other options depend on)
        self.root_options = []
        for option_name, details in self.schema.items():
            # An option is a root option if other options depend on it
            is_root = any(
                option_name in self.schema[other_option].get("depends_on", [])
                for other_option in self.schema
            )
            if is_root:
                self.root_options.append(option_name)

        # Process the schema to set all attributes
        options = self._process_schema(self.schema, args_dict)

        # Set attributes dynamically using lowercase underscore format
        for key, value in options.items():
            # Convert schema key (UPPER_CASE) to attribute name (lower_case)
            attr_name = key.lower()
            details = self.schema[key]
            setattr(self, attr_name, value)
            logger.debug(f"Set attribute {attr_name} to value: {value if not details.get('sensitive', False) else '***HIDDEN***'}")

        self.validate()

        # Setup loguru logging
        self._setup_logging()
        
        self.log()

    def _get_log_file(self, log_file: str | Path | None = None) -> Path:
        """
        Get the log file path.
        
        Priority order:
        1. Direct log_file parameter
        2. Configuration file (pyproject.toml)
        3. Default location (src/optionsconfig/logs/default.log or based on export_dir)
        
        Args:
            log_file: Optional direct path to log file
            
        Returns:
            Path to log file
        """
        # 1. Direct path parameter
        if log_file is not None:
            return Path(log_file)
        
        # 2. Configuration file (pyproject.toml)
        config_path = self._load_log_file_from_config()
        if config_path:
            return config_path
        
        # 3. Default location - determine filename based on export_dir if available
        default_dir = Path(__file__).parent / 'logs'
        
        # Try to use export_dir for filename if it exists in schema
        if 'EXPORT_DIR' in self.schema and hasattr(self, 'export_dir') and self.export_dir:
            log_filename = str(self.export_dir).replace('\\', '/').rstrip('/').split('/')[-1] + '.log'
        else:
            log_filename = 'default.log'
        
        return default_dir / log_filename
    
    def _load_log_file_from_config(self) -> Path | None:
        """Load log file path from pyproject.toml."""
        try:
            import tomllib
        except ImportError:
            try:
                import tomli as tomllib
            except ImportError:
                # Python < 3.11 and tomli not installed, skip this method
                return None
        
        config_file = Path('pyproject.toml')
        if not config_file.exists():
            return None
        
        try:
            with open(config_file, 'rb') as f:
                config = tomllib.load(f)
            
            log_file_path = config.get('tool', {}).get('optionsconfig', {}).get('log_file')
            if log_file_path:
                return Path(log_file_path)
        except Exception:
            # If any error occurs reading config, return None
            pass
        
        return None

    def _setup_logging(self) -> None:
        """Setup loguru logging to the configured log file."""
        # Ensure parent directory exists
        os.makedirs(self.log_file.parent, exist_ok=True)
        
        logger.remove()
        
        # Clear the log file before adding the handler
        with open(self.log_file, 'w') as f:
            pass
        
        my_log_level = getattr(self, 'log_level', 'DEBUG')
        logger.add(str(self.log_file), level=my_log_level, rotation="30 MB", retention="10 days", enqueue=True)
        logger.add(sys.stdout, level=my_log_level)

    def _process_schema(self, schema: dict, args_dict: dict) -> dict:
        """Process the option schema, env options, and args to get the combined options."""

        options = {}

        # Process all options in the schema
        for option_name, details in schema.items():
            # Convert arg name to attribute name (remove -- and convert - to _)
            attr_name = details["arg"].lstrip('--').replace('-', '_')
            
            # Get value in order of priority: args -> env -> default
            value = None

            logger.debug(f"Processing option: {option_name} (attr: {attr_name})")

            # 1. Check args first
            if attr_name in args_dict and args_dict[attr_name] is not None:
                value = args_dict[attr_name]
                logger.debug(f"Argument {attr_name} found in args with value: {value if not details.get('sensitive', False) else '***HIDDEN***'}")
            # 2. Check environment variable
            elif details["env"] in os.environ:
                env_value = os.environ[details["env"]]
                logger.debug(f"Environment variable {details['env']} found with value: {env_value if not details.get('sensitive', False) else '***HIDDEN***'}")
                # Convert environment string to proper type
                if details["type"] == bool:
                    value = is_truthy(env_value)
                elif details["type"] == Path:
                    value = Path(env_value) if env_value else None
                elif get_origin(details["type"]) is Literal:
                    # For Literal types, use the string value directly if it's valid
                    valid_choices = get_args(details["type"])
                    value = env_value if env_value in valid_choices else details["default"]
                else:
                    value = details["type"](env_value) if env_value else details["default"]
            # 3. Use default
            else:
                value = details["default"]
            
            # Store
            options[option_name] = value

        # If none of the root options have been explicitly set (from args or env), default all to true for ease of use
        # Check if any root option was explicitly provided (not just defaulted from schema)
        explicitly_set_root_options = []
        for root_option in self.root_options:
            attr_name = self.schema[root_option]["arg"].lstrip('--').replace('-', '_')
            # Check if it was in args or environment
            if (attr_name in args_dict and args_dict[attr_name] is not None) or \
               self.schema[root_option]["env"] in os.environ:
                explicitly_set_root_options.append(root_option)
        
        if not explicitly_set_root_options:
            # No root options were explicitly set, default all to True
            for root_option in self.root_options:
                options[root_option] = True
            logger.debug("No root options explicitly set, defaulting all to True")

        return options
    
    def validate(self) -> None:
        # Validate that options with dependencies have their requirements met
        options_as_dict = {k.upper(): v for k, v in self.__dict__.items() if k != 'root_options'}
        
        # Check each option that has dependencies
        for option_name, details in self.schema.items():
            depends_on_list = details.get("depends_on", [])
            if not depends_on_list:
                continue
            
            # Check if ANY of the dependencies are True
            any_dependency_true = any(
                options_as_dict.get(dep_option) is True
                for dep_option in depends_on_list
            )
            
            if any_dependency_true:
                value = options_as_dict.get(option_name)
                if value is None:
                    # Build a helpful error message
                    active_dependencies = [
                        dep for dep in depends_on_list
                        if options_as_dict.get(dep) is True
                    ]
                    raise ValueError(
                        f"{option_name} is required when any of the following are true: "
                        f"{', '.join(depends_on_list)}. Currently active: {', '.join(active_dependencies)}"
                    )
                logger.debug(f"Dependent option {option_name} is set to {value if not details.get('sensitive', False) else '***HIDDEN***'}")
        
    def log(self):
        """
        Logs the options.
        """
        # Dynamically log all attributes that were set from the schema
        log_lines = ["Options initialized with:"]
        
        for option_name, details in self.schema.items():
            attr_name = details["arg"].lstrip('--').replace('-', '_')
            if hasattr(self, attr_name):
                value = getattr(self, attr_name)
                # Don't log sensitive information
                if details.get("sensitive", False):
                    value = "***HIDDEN***"
                log_lines.append(f"{option_name}: {value}")
        
        logger.info("\n".join(log_lines))


# Helper to initialize OPTIONS with direct args if available
def init_options(args: Namespace | None = None, schema: dict | None = None, log_file: str | Path | None = None) -> Options:
    global OPTIONS
    OPTIONS = Options(args=args, schema=schema, log_file=log_file)
    return OPTIONS


def is_truthy(string):
    TRUE_THO = [
        True,
        'true',
        'True',
        'TRUE',
        't',
        'T',
        1,
    ]
    return string in TRUE_THO
