from typing import TypedDict, List, Optional, Any

"""
* **env** - Environment variable name (UPPER_CASE)
* **arg** - Command line argument (kebab-case with --)
* **type** - Python type (bool, str, Path, Literal)
* **default** - Default value. None means its required if any depends_on option is True
* **help** - Description text
* **section** - Logical grouping name
* **depends_on** - Optional. List of option names this option depends on (required when ANY of those options is True)
* **sensitive** - Boolean flag for password masking
"""

class OptionDefinition(TypedDict, total=False):
    env: str
    arg: str
    type: Any
    default: Any
    section: str
    help: str
    depends_on: Optional[List[str]]
    sensitive: Optional[bool]

def validate_schema(schema: dict) -> bool:
    """Validate user's OPTIONS_SCHEMA follows required format."""
    # Validation logic here
    pass