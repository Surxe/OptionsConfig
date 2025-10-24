# Schema Documentation

This document describes the `OPTIONS_SCHEMA` format and how it's loaded, validated, and used by OptionsConfig.

## Schema Format

`OPTIONS_SCHEMA` is a dictionary where each key is an option name (UPPER_CASE) and the value defines the option's properties:

```python
OPTIONS_SCHEMA = {
    "OPTION_NAME": {
        "env": "OPTION_NAME",           # Environment variable name (UPPER_CASE)
        "arg": "--option-name",          # CLI argument (kebab-case with --)
        "type": str,                     # Python type: bool, str, int, Path, Literal
        "default": "default_value",      # Default value (None if required when dependencies active)
        "section": "Section Name",       # Logical grouping for documentation
        "help": "Description text",      # Help text for CLI and docs
        "depends_on": ["OTHER_OPTION"],  # Optional: List of options this depends on
        "sensitive": False,              # Optional: Mask value in logs (for passwords)
    },
}
```

### Required Fields

- **env**: Environment variable name (must be UPPER_CASE)
- **arg**: Command-line argument (must start with `--`, use kebab-case)
- **type**: Python type (`bool`, `str`, `int`, `float`, `Path`, `Literal[...]`)
- **default**: Default value (use `None` for conditionally required options)
- **section**: Section name for grouping in documentation
- **help**: Description text shown in `--help` and generated docs

### Optional Fields

- **depends_on**: List of option names. If ANY listed option is `True`, this option becomes required (must not be `None`)
- **sensitive**: Boolean flag. When `True`, value is masked as `***HIDDEN***` in logs

## Validation Rules

The schema validator checks:

1. **Structure**: Schema must be a non-empty dictionary
2. **Required Fields**: All options must have env, arg, type, default, section, help
3. **Field Types**: env and arg must be strings
4. **Naming Conventions**:
   - `env` must be UPPER_CASE
   - `arg` must start with `--`
5. **Dependencies**: Options in `depends_on` must exist in schema
6. **Types**: depends_on must be a list if present

## Root Options Auto-True Behavior

If an option is a **root option** (other options depend on it) and NO root options are explicitly set via CLI args or environment variables, ALL root options default to `True`.

## See Also

- [options.py](src/optionsconfig/options.py) - Options class implementation
- [schema.py](src/optionsconfig/schema.py) - Schema loading and validation
- [examples/direct-pass/](examples/direct-pass/) - Example with direct schema parameter
- [examples/toml/](examples/toml/) - Example using pyproject.toml