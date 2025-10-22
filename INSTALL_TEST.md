# Installation Test

After installing `optionsconfig`, you can verify the installation by checking if the CLI is available:

## Quick Test

```bash
# Check if the command is available
optionsconfig --version

# View help
optionsconfig --help
```

## Expected Output

```
$ optionsconfig --help
usage: optionsconfig [-h] [--version] {build,validate,info} ...

OptionsConfig CLI - Generate documentation and validate schemas

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit

commands:
  Available commands

  {build,validate,info}
    build               Generate documentation files
    validate            Validate OPTIONS_SCHEMA
    info                Display schema information
```

## Test with a Schema

Create a test project to verify full functionality:

```bash
# Create test directory
mkdir optionsconfig-test
cd optionsconfig-test

# Create a simple schema
cat > options_schema.py << 'EOF'
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
EOF

# Create pyproject.toml
cat > pyproject.toml << 'EOF'
[tool.optionsconfig]
schema_module = "options_schema"
EOF

# Validate the schema
optionsconfig validate

# Show schema info
optionsconfig info

# Create .env.example with markers
cat > .env.example << 'EOF'
# My Application Configuration
# BEGIN_OPTIONS_CONFIG
# END_OPTIONS_CONFIG
EOF

# Generate documentation
optionsconfig build env

# Check the result
cat .env.example
```

If everything works, you should see:
- ✓ Schema is valid
- Schema information displayed
- .env.example populated with your options

## Development Installation

If you're developing the package:

```bash
# Install in editable mode
pip install -e .

# Or with development dependencies
pip install -e ".[dev]"

# Test the CLI directly
python -m optionsconfig.cli --help
```
