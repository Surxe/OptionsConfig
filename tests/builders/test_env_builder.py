#!/usr/bin/env python3
"""Test script for core.py functionality"""

import sys
from pathlib import Path

# Add src to path for local testing
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from optionsconfig.builders.env_builder import EnvBuilder

# Import the test schema from this directory
from options_schema import OPTIONS_SCHEMA

def test(env_example_path: Path):
    # Pass the schema directly instead of relying on auto-discovery
    EnvBuilder(schema=OPTIONS_SCHEMA, env_example_path=env_example_path).build()

    expected_lines = [
        "# Use forward slashes \"/\" in paths for compatibility across platforms",
        "",
        "# Parse",
        "# Whether to parse the game files.",
        "SHOULD_PARSE=\"False\"",
        "",
        "# Name of the game to parse.",
        "# Required when SHOULD_PARSE is True",
        "GAME_TO_PARSE=\"WRFrontiers\"",
        "",
    ]

    expected_content = "\n".join(expected_lines)
    genned_content = read_genned_env_example(env_example_path)
    assert genned_content.strip() == expected_content.strip(), "Generated .env.example content does not match expected content."

def read_genned_env_example(env_example_path: Path):
    with open(env_example_path, 'r', encoding='utf-8') as f:
        return f.read()

if __name__ == "__main__":
    env_example_path = Path('tests/builders/env.example')
    test(env_example_path)
    print("All tests completed!")