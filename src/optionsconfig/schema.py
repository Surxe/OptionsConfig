"""
Schema loading and validation for OPTIONS_SCHEMA.

OPTIONS_SCHEMA format:
* **env** - Environment variable name (UPPER_CASE)
* **arg** - Command line argument (kebab-case with --)
* **type** - Python type (bool, str, Path, Literal)
* **default** - Default value. None means its required if any depends_on option is True
* **help** - Description text
* **section** - Logical grouping name
* **depends_on** - Optional. List of option names this option depends on (required when ANY of those options is True)
* **sensitive** - Boolean flag for password masking
"""

from typing import TypedDict, List, Optional, Any
from pathlib import Path


class OptionDefinition(TypedDict, total=False):
    env: str
    arg: str
    type: Any
    default: Any
    section: str
    help: str
    depends_on: Optional[List[str]]
    sensitive: Optional[bool]


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
        return schema
    
    # 2. Configuration file (pyproject.toml)
    config_schema = _load_schema_from_config()
    if config_schema:
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
    except Exception:
        # If any error occurs reading config or importing module, return None
        pass
    
    return None


def validate_schema(schema: dict) -> bool:
    """Validate user's OPTIONS_SCHEMA follows required format."""
    pass