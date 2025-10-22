# Schema Loading Guide

## Overview

The `optionsconfig` package supports two methods for loading the `OPTIONS_SCHEMA`:

1. **Direct schema dict** - Pass the schema directly when creating instances
2. **Configuration file** - Define the schema module path in `pyproject.toml`

## Method 1: Direct Schema Dict

Pass your schema directly to any class that needs it:

```python
from optionsconfig import Options, ArgumentWriter

# Define your schema
MY_SCHEMA = {
    "DEBUG": {
        "env": "DEBUG",
        "arg": "--debug",
        "type": bool,
        "default": False,
        "section": "General",
        "help": "Enable debug mode"
    }
}

# Pass it directly
options = Options(schema=MY_SCHEMA)
writer = ArgumentWriter(schema=MY_SCHEMA)
```

## Method 2: Configuration File (Recommended)

Define the schema module path in your `pyproject.toml`:

### Step 1: Create your schema file

```python
# File: config/options_schema.py
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

### Step 2: Configure pyproject.toml

```toml
[tool.optionsconfig]
schema_module = "config.options_schema"
```

The module path should be:
- Importable from your project root
- Use dot notation for nested modules
- Point to a module with `OPTIONS_SCHEMA` defined

### Step 3: Use without explicit schema

```python
from optionsconfig import Options, ArgumentWriter

# Schema is automatically loaded from pyproject.toml
options = Options()
writer = ArgumentWriter()
```

## Installing tomli for Python < 3.11

If you're using Python < 3.11, install the `tomli` package:

```bash
pip install tomli
```

Or include it in your project dependencies:

```toml
[project]
dependencies = [
    "optionsconfig",
    "tomli>=2.0.0; python_version < '3.11'",
]
```

## Common Module Paths

Here are examples of valid `schema_module` values:

| File Location | schema_module Value |
|--------------|-------------------|
| `options_schema.py` (root) | `"options_schema"` |
| `config/options_schema.py` | `"config.options_schema"` |
| `src/options_schema.py` | `"src.options_schema"` |
| `myapp/config/schema.py` | `"myapp.config.schema"` |

## Priority Order

When loading schemas, the following priority is used:

1. **Direct schema parameter** - If you pass `schema=` to `Options()` or `ArgumentWriter()`
2. **pyproject.toml** - If `[tool.optionsconfig] schema_module` is configured
3. **ImportError** - If neither is found, an error is raised with helpful instructions

## Error Messages

If no schema is found, you'll see:

```
ImportError: No OPTIONS_SCHEMA found.
Please either:
1. Pass schema directly: Options(schema=YOUR_SCHEMA)
2. Configure [tool.optionsconfig] schema_module in pyproject.toml
```

## Examples

### Example 1: Simple Project

```
myproject/
├── pyproject.toml
├── options_schema.py
└── main.py
```

**pyproject.toml:**
```toml
[tool.optionsconfig]
schema_module = "options_schema"
```

**main.py:**
```python
from optionsconfig import Options
options = Options()  # Automatically loads from options_schema.py
```

### Example 2: Package Structure

```
myproject/
├── pyproject.toml
└── myapp/
    ├── __init__.py
    ├── config/
    │   ├── __init__.py
    │   └── options_schema.py
    └── main.py
```

**pyproject.toml:**
```toml
[tool.optionsconfig]
schema_module = "myapp.config.options_schema"
```

**main.py:**
```python
from optionsconfig import Options
options = Options()  # Automatically loads from myapp/config/options_schema.py
```

### Example 3: Testing with Custom Schema

```python
import pytest
from optionsconfig import Options

def test_custom_config():
    test_schema = {
        "TEST_VAR": {
            "env": "TEST_VAR",
            "arg": "--test-var",
            "type": str,
            "default": "test",
            "section": "Testing",
            "help": "Test variable"
        }
    }
    
    options = Options(schema=test_schema)
    assert options.test_var == "test"
```