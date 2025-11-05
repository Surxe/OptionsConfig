from typing import TypedDict, List, Optional, Any
from pathlib import Path


class OptionDefinition(TypedDict, total=False):
    env: str # Environment variable name (recommended UPPER_CASE)
    arg: str # Command line argument (kebab-case with --)
    var: Optional[str] # Variable name in Python code (recommended snake_case)
    type: Any # Python type (bool, str, Path, Literal)
    default: Any # Default value. None means its required if any depends_on option is True
    section: str # Logical grouping name
    help: str # Description text
    depends_on: Optional[List[str]] # List of option names this option depends on (required when ANY of those options are True)
    sensitive: Optional[bool] # Boolean flag for password masking


def get_schema(schema: dict | None = None) -> dict:
    """
    Load OPTIONS_SCHEMA from available sources.
    
    Priority order:
    1. Direct schema dict passed as argument
    2. Configuration file (pyproject.toml)
    
    Args:
        schema: Direct schema dict to use
    
    Returns:
        The OPTIONS_SCHEMA dictionary
    
    Raises:
        ImportError: If no schema can be found
    """
    # 1. Direct schema dict
    if schema is not None:
        schema = default_schema_details(schema)
        validate_schema(schema)
        return schema
    
    # 2. Configuration file (pyproject.toml)
    config_schema = _load_schema_from_config()
    if config_schema:
        config_schema = default_schema_details(config_schema)
        validate_schema(config_schema)
        return config_schema
    
    raise ImportError(
        "No OPTIONS_SCHEMA found.\n"
        "Please either:\n"
        "1. Pass schema directly: Options(schema=YOUR_SCHEMA)\n"
        "2. Configure [tool.optionsconfig] schema_module in pyproject.toml"
    )


def _load_schema_from_config() -> dict | None:
    """Load schema module path from pyproject.toml."""
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
        
        schema_module = config.get('tool', {}).get('optionsconfig', {}).get('schema_module')
        if schema_module:
            module = __import__(schema_module, fromlist=['OPTIONS_SCHEMA'])
            return module.OPTIONS_SCHEMA
    except ImportError as e:
        raise ImportError(f"Could not import schema module '{schema_module}': {e}")
    
    return None


def load_schema() -> dict | None:
    """
    Load OPTIONS_SCHEMA from available sources without raising exceptions.
    
    Returns:
        The OPTIONS_SCHEMA dictionary or None if not found
    """
    try:
        return get_schema()
    except ImportError:
        return None
    

def default_schema_details(schema: dict) -> dict:
    defaulted_schema = schema.copy()
    for option_name, details in schema.items():
        if "sensitive" not in details:
            defaulted_schema[option_name]["sensitive"] = False
        if "depends_on" not in details:
            defaulted_schema[option_name]["depends_on"] = []
        if "var" not in details:
            defaulted_schema[option_name]["var"] = option_name.lower()
            print(f"Defaulted 'var' for option '{option_name}' to '{option_name.lower()}'")
    return defaulted_schema


def validate_schema(schema: dict) -> list[str]:
    """
    Validate user's OPTIONS_SCHEMA follows required format.
    
    Args:
        schema: The OPTIONS_SCHEMA dictionary to validate
    
    Returns:
        List of error messages (empty list if valid)
    """
    errors = []
    
    if not isinstance(schema, dict):
        errors.append("Schema must be a dictionary")
        return errors
    
    if not schema:
        errors.append("Schema is empty")
        return errors
    
    required_fields = ["env", "arg", "var", "type", "default", "section", "help", "sensitive", "depends_on"] # optionals are defaulted beforehand
    
    for option_name, details in schema.items():
        if not isinstance(details, dict):
            errors.append(f"{option_name}: Option definition must be a dictionary")
            continue
        
        # Check required fields
        for field in required_fields:
            if field not in details:
                errors.append(f"{option_name}: Missing required field '{field}'")
        
        # Validate env variable format
        if "env" in details:
            env = details["env"]
            if not isinstance(env, str):
                errors.append(f"{option_name}: 'env' must be a string")
            elif not env.isupper():
                errors.append(f"{option_name}: 'env' should be UPPER_CASE (got '{env}')")
        
        # Validate arg format
        if "arg" in details:
            arg = details["arg"]
            if not isinstance(arg, str):
                errors.append(f"{option_name}: 'arg' must be a string")
            elif not arg.startswith("--"):
                errors.append(f"{option_name}: 'arg' should start with '--' (got '{arg}')")
        
        # Validate depends_on
        if "depends_on" in details:
            depends_on = details["depends_on"]
            if not isinstance(depends_on, list):
                errors.append(f"{option_name}: 'depends_on' must be a list")
            else:
                for dep in depends_on:
                    if dep not in schema:
                        errors.append(f"{option_name}: depends on non-existent option '{dep}'")
    
    return errors