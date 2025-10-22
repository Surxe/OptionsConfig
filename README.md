# OptionsConfig

Unified configuration management for Python applications. Define your configuration schema once, use it everywhere.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- **📋 Single Schema Definition** - Define configuration options once in a typed schema
- **🔧 Multiple Input Sources** - Supports CLI arguments and environment `.env` files
- **📚 Auto-Generate Documentation** - Create `.env.example` and README sections automatically
- **⚙️ Type Safety** - Built-in type checking with Python type hints
- **🔗 Dependency Management** - Define relationships between configuration options
- **📦 TOML Configuration** - Load schema from `pyproject.toml` for cleaner code

## Installation

```bash
pip install optionsconfig
```

For Python < 3.11, also install TOML support:
```bash
pip install optionsconfig[toml]
```

After installation, the `optionsconfig` command will be available in your terminal.

## Quick Start

### 1. Define Your Schema

Create an `options_schema.py` file in your project:

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
    },
    "API_KEY": {
        "env": "API_KEY",
        "arg": "--api-key",
        "type": str,
        "default": None,
        "section": "API",
        "help": "API key for authentication"
    }
}
```

### 2. Configure pyproject.toml

```toml
[tool.optionsconfig]
schema_module = "options_schema"
```

### 3. Use in Your Application

```python
from optionsconfig import Options

# Automatically loads schema from pyproject.toml
options = Options()

# Access configuration values
if options.debug:
    print(f"API Key: {options.api_key}")
```

### 4. Generate Documentation

```bash
# Generate .env.example and update README.md
optionsconfig build all
```

## Core Components

### Options
Manages configuration from multiple sources with priority: CLI args > .env file > defaults

```python
from optionsconfig import Options

options = Options()  # Loads schema from pyproject.toml
print(options.debug)
```

### ArgumentWriter
Generates argparse arguments from schema

```python
from optionsconfig import ArgumentWriter
import argparse

parser = argparse.ArgumentParser()
writer = ArgumentWriter()
writer.add_arguments(parser)
args = parser.parse_args()
```

### EnvBuilder
Generates `.env.example` files from schema

```python
from optionsconfig import EnvBuilder

builder = EnvBuilder()
builder.build()  # Creates .env.example
```

### ReadmeBuilder
Generates configuration documentation for README

```python
from optionsconfig import ReadmeBuilder

builder = ReadmeBuilder()
builder.build()  # Updates README.md between markers
```

## Schema Definition

Each option in your schema requires:

- `env` - Environment variable name
- `arg` - Command-line argument name
- `type` - Python type (bool, str, int, float, Path, Literal)
- `default` - Default value
- `section` - Documentation section grouping
- `help` - Help text description

Optional fields:
- `depends_on` - List of required option names
- `choices` - Valid values for Literal types

## Configuration Loading

See [SCHEMA_LOADING.md](SCHEMA_LOADING.md) for detailed information on:
- Direct schema vs. configuration file loading
- Module path configuration
- Priority order
- Common patterns and examples

## Documentation Generation

### Command Line Interface

After installing the package, use the `optionsconfig` command:

```bash
# Generate .env.example
optionsconfig build env

# Update README.md
optionsconfig build readme

# Generate all documentation
optionsconfig build all

# Validate your schema
optionsconfig validate

# Show schema information
optionsconfig info
optionsconfig info -v  # verbose output
```

### Programmatic API

#### .env.example

Place options between special markers in your `.env.example`:

```bash
# .env.example
# BEGIN_OPTIONS_CONFIG
# END_OPTIONS_CONFIG
```

Run `EnvBuilder().build()` or use the CLI to populate the section.

#### README.md

Place options between special markers in your `README.md`:

```markdown
<!-- BEGIN_GENERATED_OPTIONS -->
<!-- END_GENERATED_OPTIONS -->
```

Run `ReadmeBuilder().build()` or use the CLI to populate the section.

## Testing

The package includes comprehensive test coverage (65 tests):

```bash
# Run all tests
python -m unittest discover -s tests -p "test_*.py"

# Run specific test modules
python -m unittest tests.options.test_options
python -m unittest tests.builders.env_builder.test_env_builder
```

## Examples

### Complete Application Setup

```python
# main.py
from optionsconfig import Options, ArgumentWriter
import argparse

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser()
    writer = ArgumentWriter()
    writer.add_arguments(parser)
    
    # Parse arguments and load options
    args = parser.parse_args()
    options = Options(args)
    
    # Use configuration
    if options.debug:
        print("Debug mode enabled")
    
    return options

if __name__ == "__main__":
    main()
```

### Generate Documentation with CLI

```bash
# Validate your schema first
optionsconfig validate

# Generate .env.example
optionsconfig build env

# Update README.md with options documentation
optionsconfig build readme

# Or generate everything at once
optionsconfig build all

# View schema information
optionsconfig info
```

### Generate Documentation Programmatically

```python
# scripts/build_docs.py
from optionsconfig import EnvBuilder, ReadmeBuilder

def build_all():
    """Generate all configuration documentation"""
    env_builder = EnvBuilder()
    readme_builder = ReadmeBuilder()
    
    env_builder.build()
    readme_builder.build()
    
    print("Documentation generated successfully!")

if __name__ == "__main__":
    build_all()
```

## Requirements

- Python >= 3.8
- python-dotenv >= 0.19.0
- loguru >= 0.6.0
- tomli >= 2.0.0 (Python < 3.11 only)

## License

MIT License - see LICENSE file for details

## Contributing

Contributions welcome! TODO

## Links

- **Repository**: https://github.com/Surxe/OptionsConfig
- **Documentation**: [SCHEMA_LOADING.md](SCHEMA_LOADING.md)