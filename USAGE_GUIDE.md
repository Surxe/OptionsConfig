# Using OptionsConfig in Your Repository

This guide shows you how to integrate OptionsConfig into your own projects.

## Step 1: Install OptionsConfig

### Option A: Install from PyPI (when published)
```bash
pip install optionsconfig
```

### Option B: Install from Local Repository
```bash
# From the OptionsConfig repository directory
pip install -e /path/to/OptionsConfig

# Or install directly from Git
pip install git+https://github.com/Surxe/OptionsConfig.git
```

### Option C: Add to requirements.txt
```txt
# requirements.txt
optionsconfig>=0.1.0

# Or from Git
# git+https://github.com/Surxe/OptionsConfig.git
```

Then install:
```bash
pip install -r requirements.txt
```

## Step 2: Create Your Options Schema

In your project root, create `options_schema.py`:

```python
# options_schema.py
from typing import Literal
from pathlib import Path

OPTIONS_SCHEMA = {
    "DEBUG": {
        "env": "DEBUG",
        "arg": "--debug",
        "type": bool,
        "default": False,
        "section": "General",
        "help": "Enable debug mode"
    },
    "LOG_LEVEL": {
        "env": "LOG_LEVEL",
        "arg": "--log-level",
        "type": Literal["DEBUG", "INFO", "WARNING", "ERROR"],
        "default": "INFO",
        "section": "General",
        "help": "Logging level"
    },
    "DATABASE_URL": {
        "env": "DATABASE_URL",
        "arg": "--database-url",
        "type": str,
        "default": None,
        "section": "Database",
        "help": "Database connection string"
    },
    "ENABLE_CACHE": {
        "env": "ENABLE_CACHE",
        "arg": "--enable-cache",
        "type": bool,
        "default": False,
        "section": "Performance",
        "help": "Enable caching layer"
    },
    "CACHE_DIR": {
        "env": "CACHE_DIR",
        "arg": "--cache-dir",
        "type": Path,
        "default": None,
        "section": "Performance",
        "depends_on": ["ENABLE_CACHE"],
        "help": "Directory for cache files"
    },
    "API_KEY": {
        "env": "API_KEY",
        "arg": "--api-key",
        "type": str,
        "default": None,
        "section": "API",
        "sensitive": True,
        "help": "API authentication key"
    }
}
```

## Step 3: Configure pyproject.toml

Add the OptionsConfig configuration:

```toml
# pyproject.toml
[project]
name = "your-project"
version = "1.0.0"
dependencies = [
    "optionsconfig>=0.1.0",
    # ... other dependencies
]

[tool.optionsconfig]
schema_module = "options_schema"

# Optional: Custom paths
# env_example_path = ".env.example"
# readme_path = "README.md"
```

## Step 4: Use Options in Your Code

### Basic Usage

```python
# main.py
from optionsconfig import Options

def main():
    # Load configuration automatically
    options = Options()
    
    # Access options as attributes (lowercase with underscores)
    if options.debug:
        print("Debug mode is ON")
    
    print(f"Log level: {options.log_level}")
    
    if options.enable_cache:
        print(f"Cache directory: {options.cache_dir}")

if __name__ == "__main__":
    main()
```

### With Command Line Arguments

```python
# main.py
from optionsconfig import Options, ArgumentWriter
import argparse

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description="My Application")
    
    # Add options from schema
    writer = ArgumentWriter()
    writer.add_arguments(parser)
    
    # Parse command line arguments
    args = parser.parse_args()
    
    # Initialize options with CLI args
    options = Options(args)
    
    # Use your options
    print(f"Debug: {options.debug}")
    print(f"Database: {options.database_url}")

if __name__ == "__main__":
    main()
```

### With Custom Schema Location

```python
# If your schema is in a different location
from optionsconfig import Options

# Import your schema
from config.settings import MY_OPTIONS_SCHEMA

# Pass it directly
options = Options(schema=MY_OPTIONS_SCHEMA)
```

## Step 5: Set Up Environment Files

### Create .env.example Template

```bash
# .env.example
# This file will be auto-generated from your schema

# BEGIN_OPTIONS_CONFIG
# END_OPTIONS_CONFIG
```

### Generate .env.example

```bash
# Using CLI
optionsconfig build env

# Or in Python
from optionsconfig import EnvBuilder
builder = EnvBuilder()
builder.build()
```

### Create Your Local .env

```bash
# Copy the example
cp .env.example .env

# Edit with your actual values
nano .env
```

## Step 6: Generate Documentation

### Add README Markers

```markdown
<!-- README.md -->
# My Project

## Configuration Options

<!-- BEGIN_GENERATED_OPTIONS -->
<!-- END_GENERATED_OPTIONS -->
```

### Generate Documentation

```bash
# Generate all documentation
optionsconfig build all

# Or individual files
optionsconfig build env      # .env.example
optionsconfig build readme   # README.md

# Validate your schema
optionsconfig validate

# View schema info
optionsconfig info -v
```

## Step 7: Running Your Application

### With Environment Variables

```bash
# Set environment variables
export DEBUG=True
export LOG_LEVEL=DEBUG
export DATABASE_URL="postgresql://localhost/mydb"

# Run your app
python main.py
```

### With .env File

```bash
# .env file is automatically loaded
python main.py
```

### With Command Line Arguments

```bash
python main.py --debug --log-level DEBUG --database-url "postgresql://localhost/mydb"
```

### Priority Order

1. Command line arguments (highest priority)
2. Environment variables from .env file
3. Default values from schema (lowest priority)

## Complete Example Project Structure

```
your-project/
├── .env                      # Local config (gitignored)
├── .env.example             # Template (committed)
├── README.md                # With generated docs
├── pyproject.toml           # Package config
├── requirements.txt         # Dependencies
├── options_schema.py        # Your schema definition
├── main.py                  # Your application
└── src/
    └── your_module/
        └── __init__.py
```

## Example: Complete Integration

Here's a full working example:

**pyproject.toml:**
```toml
[project]
name = "myapp"
version = "1.0.0"
dependencies = [
    "optionsconfig>=0.1.0",
    "requests>=2.28.0",
]

[tool.optionsconfig]
schema_module = "options_schema"
```

**options_schema.py:**
```python
OPTIONS_SCHEMA = {
    "API_URL": {
        "env": "API_URL",
        "arg": "--api-url",
        "type": str,
        "default": "https://api.example.com",
        "section": "API",
        "help": "Base API URL"
    },
    "API_KEY": {
        "env": "API_KEY",
        "arg": "--api-key",
        "type": str,
        "default": None,
        "section": "API",
        "sensitive": True,
        "help": "API authentication key"
    },
    "TIMEOUT": {
        "env": "TIMEOUT",
        "arg": "--timeout",
        "type": int,
        "default": 30,
        "section": "API",
        "help": "Request timeout in seconds"
    }
}
```

**main.py:**
```python
from optionsconfig import Options, ArgumentWriter
import argparse
import requests

def fetch_data(options):
    """Fetch data from API using configuration."""
    headers = {"Authorization": f"Bearer {options.api_key}"}
    response = requests.get(
        options.api_url,
        headers=headers,
        timeout=options.timeout
    )
    return response.json()

def main():
    # Set up CLI
    parser = argparse.ArgumentParser(description="My API Client")
    writer = ArgumentWriter()
    writer.add_arguments(parser)
    args = parser.parse_args()
    
    # Load configuration
    options = Options(args)
    
    # Use configuration
    try:
        data = fetch_data(options)
        print(f"Fetched {len(data)} items")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

**.env.example:**
```bash
# BEGIN_OPTIONS_CONFIG
# This will be auto-generated
# END_OPTIONS_CONFIG
```

**Generate documentation:**
```bash
# Generate all docs
optionsconfig build all

# Run your app
python main.py --api-key "your-secret-key"
```

## Tips and Best Practices

### 1. Keep Schema in Root
Place `options_schema.py` in your project root for easy access.

### 2. Gitignore Your .env
```gitignore
# .gitignore
.env
*.log
__pycache__/
```

### 3. Document Dependencies
Use `depends_on` for conditional options:
```python
"ENABLE_FEATURE": {
    "type": bool,
    "default": False,
    # ...
},
"FEATURE_CONFIG": {
    "depends_on": ["ENABLE_FEATURE"],  # Required when ENABLE_FEATURE is True
    "default": None,
    # ...
}
```

### 4. Mark Sensitive Data
```python
"PASSWORD": {
    "sensitive": True,  # Will be masked in logs
    # ...
}
```

### 5. Use Type Hints
```python
from typing import Literal
from pathlib import Path

"MODE": {
    "type": Literal["dev", "staging", "prod"],
    # ...
},
"OUTPUT_DIR": {
    "type": Path,  # Automatically converted to Path object
    # ...
}
```

### 6. Validate Before Deployment
```bash
# In CI/CD pipeline
optionsconfig validate || exit 1
```

### 7. Generate Docs Automatically
```bash
# Add to your build scripts or pre-commit hooks
optionsconfig build all
git add .env.example README.md
```

## Troubleshooting

### "No OPTIONS_SCHEMA found"
- Ensure `options_schema.py` exists in project root
- Check `pyproject.toml` has correct `schema_module` path
- Try passing schema directly: `Options(schema=YOUR_SCHEMA)`

### "Module not found"
- Install optionsconfig: `pip install optionsconfig`
- Or install in development mode: `pip install -e /path/to/OptionsConfig`

### CLI Command Not Found
- Reinstall: `pip install --force-reinstall optionsconfig`
- Use module form: `python -m optionsconfig.cli`
- Check PATH includes Python scripts directory

### Schema Validation Errors
```bash
# Check what's wrong
optionsconfig validate
```

Common issues:
- Missing required fields (env, arg, type, default, section, help)
- Env variables not UPPER_CASE
- Args not starting with `--`
- Invalid `depends_on` references

## Getting Help

- View CLI help: `optionsconfig --help`
- View command help: `optionsconfig build --help`
- Check schema: `optionsconfig info -v`
- Validate: `optionsconfig validate`

## Next Steps

1. ✅ Install OptionsConfig
2. ✅ Create your `options_schema.py`
3. ✅ Configure `pyproject.toml`
4. ✅ Use `Options()` in your code
5. ✅ Generate documentation with `optionsconfig build all`
6. 🚀 Deploy your application!
