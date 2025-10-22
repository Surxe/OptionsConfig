#!/usr/bin/env python3
"""Test script for EnvBuilder functionality"""

import sys
import unittest
from pathlib import Path

# Add paths
src_path = str(Path(__file__).parent.parent.parent.parent / "src")
local_path = str(Path(__file__).parent)
if src_path not in sys.path:
    sys.path.insert(0, src_path)
if local_path not in sys.path:
    sys.path.insert(0, local_path)

from optionsconfig.builders.env_builder import EnvBuilder
from env_builder_schema import OPTIONS_SCHEMA


class TestEnvBuilder(unittest.TestCase):
    """Test cases for EnvBuilder."""
    
    def setUp(self):
        """Set up test file path."""
        self.env_example_path = Path('tests/builders/env_builder/env.example')
    
    def test_build_env_example(self):
        """Test that EnvBuilder generates correct .env.example content."""
        # Pass the schema directly instead of relying on auto-discovery
        EnvBuilder(schema=OPTIONS_SCHEMA, env_example_path=self.env_example_path).build()
        
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
        genned_content = self._read_genned_env_example()
        self.assertEqual(genned_content.strip(), expected_content.strip(), 
                        "Generated .env.example content does not match expected content.")
    
    def _read_genned_env_example(self):
        """Read generated .env.example file."""
        with open(self.env_example_path, 'r', encoding='utf-8') as f:
            return f.read()


if __name__ == "__main__":
    unittest.main()