# OptionsConfig Quick Reference

## Installation

```bash
# From PyPI (when published)
pip install optionsconfig

# From Git
pip install git+https://github.com/Surxe/OptionsConfig.git

# Local development
pip install -e /path/to/OptionsConfig
```

## Setup (3 Steps)

### 1. Create Schema
```python
# options_schema.py
OPTIONS_SCHEMA = {
    "DEBUG": {
        "env": "DEBUG",
        "arg": "--debug",
        "type": bool,
        "default": False,
        "section": "General",
        "help": "Enable debug mode"
    }
}
```

### 2. Configure pyproject.toml
```toml
[tool.optionsconfig]
schema_module = "options_schema"
```

### 3. Use in Code
```python
from optionsconfig import Options
options = Options()
print(options.debug)
```

## CLI Commands

```bash
# Validate schema
optionsconfig validate

# View schema info
optionsconfig info
optionsconfig info -v

# Generate .env.example
optionsconfig build env

# Update README.md
optionsconfig build readme

# Generate all docs
optionsconfig build all

# Help
optionsconfig --help
optionsconfig build --help
```

## Python API

### Basic Usage
```python
from optionsconfig import Options

# Auto-load from pyproject.toml
options = Options()

# Access as attributes (lowercase)
print(options.debug)
print(options.api_key)
```

### With CLI Arguments
```python
from optionsconfig import Options, ArgumentWriter
import argparse

parser = argparse.ArgumentParser()
ArgumentWriter().add_arguments(parser)
args = parser.parse_args()
options = Options(args)
```

### With Custom Schema
```python
from optionsconfig import Options

MY_SCHEMA = {...}
options = Options(schema=MY_SCHEMA)
```

### Generate Documentation
```python
from optionsconfig import EnvBuilder, ReadmeBuilder

# Generate .env.example
EnvBuilder().build()

# Update README.md
ReadmeBuilder().build()
```

## Schema Fields

### Required
- `env`: Environment variable name (UPPER_CASE)
- `arg`: CLI argument (--kebab-case)
- `type`: Python type (bool, str, int, float, Path, Literal)
- `default`: Default value
- `section`: Documentation grouping
- `help`: Description text

### Optional
- `depends_on`: List of required option names
- `sensitive`: Boolean for password masking

## Configuration Priority

1. **CLI arguments** (highest)
2. **Environment variables** (.env file)
3. **Default values** (schema) (lowest)

## File Markers

### .env.example
```bash
# BEGIN_OPTIONS_CONFIG
# Auto-generated content goes here
# END_OPTIONS_CONFIG
```

### README.md
```markdown
<!-- BEGIN_GENERATED_OPTIONS -->
Auto-generated content goes here
<!-- END_GENERATED_OPTIONS -->
```

## Common Patterns

### Conditional Options
```python
"ENABLE_FEATURE": {
    "type": bool,
    "default": False,
    # ...
},
"FEATURE_CONFIG": {
    "depends_on": ["ENABLE_FEATURE"],
    "default": None,
    # ...
}
```

### Sensitive Data
```python
"API_KEY": {
    "sensitive": True,  # Masked in logs
    "default": None,
    # ...
}
```

### Literal Types
```python
from typing import Literal

"LOG_LEVEL": {
    "type": Literal["DEBUG", "INFO", "WARNING", "ERROR"],
    "default": "INFO",
    # ...
}
```

### Path Types
```python
from pathlib import Path

"OUTPUT_DIR": {
    "type": Path,
    "default": Path("./output"),
    # ...
}
```

## Usage Examples

### Environment Variables
```bash
export DEBUG=True
export API_KEY="secret"
python main.py
```

### .env File
```bash
# .env
DEBUG=True
API_KEY=secret
```

### CLI Arguments
```bash
python main.py --debug --api-key secret
```

### Mixed
```bash
# .env has defaults, override with CLI
python main.py --debug
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No schema found | Check `pyproject.toml` `schema_module` or pass schema directly |
| Module not found | Run `pip install optionsconfig` |
| CLI not found | Use `python -m optionsconfig.cli` or check PATH |
| Validation fails | Run `optionsconfig validate` to see errors |
| Wrong attribute name | Use lowercase with underscores: `options.my_option` |

## Full Documentation

- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - Complete integration guide
- **[SCHEMA_LOADING.md](SCHEMA_LOADING.md)** - Schema configuration details
- **[INSTALL_TEST.md](INSTALL_TEST.md)** - Installation verification
- **[README.md](README.md)** - Package overview
