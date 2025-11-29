# Schema Documentation

This document describes the `OPTIONS_SCHEMA` format and how it's loaded, validated, and used by OptionsConfig.

## Schema Format

`OPTIONS_SCHEMA` is a dictionary where each key is an option name (UPPER_CASE) and the value defines the option's properties:

```python
OPTIONS_SCHEMA = {
    "OPTION_NAME": {
        "env": "OPTION_NAME",                         # Environment variable name (recommended UPPER_CASE)
        "arg": "--option-name",                       # CLI argument (kebab-case with --)
        "var": "option_name",                         # Optional: Python variable (recommended snake_case, defaults to OPTION_NAME.lower())
        "type": str,                                  # Python type: bool, str, int, Path, Literal
        "default": "default_value",                   # Default value (None if required when dependencies active)
        "section": "Section Name",                    # Logical grouping for documentation
        "help": "Description text",                   # Help text for CLI and docs
        "help_extended": "Extended description text": # Optional: Extended help text for the README only
        "links": {"link_name": "link_url"}            # Optional: Links to be included in the README only
        "example": "example value"                    # Optional: Example value for the docs only
        "depends_on": ["OTHER_OPTION"],               # Optional: List of options this depends on. OPTION_NAME is required only if one or more of their dependencies is true
        "sensitive": True,                            # Optional: Mask value in logs (for passwords)
    },
}
```

## Validation Rules

The schema validator checks:

1. **Structure**: Schema must be a non-empty dictionary
2. **Required Fields**: All options must have env, arg, type, default, section, help
3. **Field Types**: env and arg must be strings
4. **Naming Conventions**:
   - `arg` must start with `--`
5. **Dependencies**: Options in `depends_on` must exist in schema
6. **Types**: depends_on must be a list if present

## Boolean Arguments

For options defined with `"type": bool`, the command-line argument behaves as follows:

| Command | Result | Notes |
|---------|--------|-------|
| `python run.py --option-name` | `True` | Acts as a flag |
| `python run.py --option-name true` | `True` | Explicit value (case-insensitive) |
| `python run.py --option-name false` | `False` | Explicit value (case-insensitive) |
| `python run.py` | `default` | Uses the default value from schema |

Supported truthy values: `yes`, `true`, `t`, `y`, `1`
Supported falsy values: `no`, `false`, `f`, `n`, `0`

## Root Options Auto-True Behavior

If an option is a **root option** (other options depend on it) and NO root options are explicitly set via CLI args or environment variables, ALL root options default to `True`.

## See Also

- [options.py](src/optionsconfig/options.py) - Options class implementation
- [schema.py](src/optionsconfig/schema.py) - Schema loading and validation
- [examples/toml/](examples/toml/) - Example using pyproject.toml