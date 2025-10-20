# In src/optionsconfig/__init__.py
from .core import Options, ArgumentWriter, init_options
from .schema import validate_schema, OptionDefinition
from .builders.env_builder import generate_env_example, update_env_example
from .builders.readme_builder import generate_readme_options

__version__ = "1.0.0"
__all__ = [
    "Options",
    "ArgumentWriter", 
    "init_options",
    "validate_schema",
    "OptionDefinition",
    "generate_env_example",
    "update_env_example",
    "generate_readme_options"
]