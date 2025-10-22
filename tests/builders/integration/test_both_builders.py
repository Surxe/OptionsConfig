#!/usr/bin/env python3
"""Test script for both builders"""

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

from optionsconfig.builders import EnvBuilder, ReadmeBuilder
from integration_schema import OPTIONS_SCHEMA


class TestBothBuilders(unittest.TestCase):
    """Test cases for both EnvBuilder and ReadmeBuilder together."""
    
    def setUp(self):
        """Set up test file paths."""
        self.env_path = Path('tests/builders/integration/test_both.env.example')
        self.readme_path = Path('tests/builders/integration/test_both_README.md')
    
    def test_both_builders(self):
        """Test both EnvBuilder and ReadmeBuilder together."""
        # Create a test README with markers
        test_readme_content = """# Test README

<!-- BEGIN_GENERATED_OPTIONS -->
<!-- END_GENERATED_OPTIONS -->
"""
        
        with open(self.readme_path, 'w', encoding='utf-8') as f:
            f.write(test_readme_content)
        
        # Test EnvBuilder
        result = EnvBuilder(schema=OPTIONS_SCHEMA, env_example_path=self.env_path).build()
        self.assertTrue(result, "EnvBuilder failed")
        
        # Test ReadmeBuilder
        result = ReadmeBuilder(schema=OPTIONS_SCHEMA, readme_path=self.readme_path).build()
        self.assertTrue(result, "ReadmeBuilder failed")
        
        # Verify both files exist
        self.assertTrue(self.env_path.exists(), "env.example was not created")
        self.assertTrue(self.readme_path.exists(), "README.md was not created")
        
        # Verify env content
        with open(self.env_path, 'r', encoding='utf-8') as f:
            env_content = f.read()
            self.assertIn('SHOULD_PARSE', env_content, "SHOULD_PARSE not in env.example")
            self.assertIn('GAME_TO_PARSE', env_content, "GAME_TO_PARSE not in env.example")
        
        # Verify readme content
        with open(self.readme_path, 'r', encoding='utf-8') as f:
            readme_content = f.read()
            self.assertIn('**SHOULD_PARSE**', readme_content, "SHOULD_PARSE not in README")
            self.assertIn('**GAME_TO_PARSE**', readme_content, "GAME_TO_PARSE not in README")


if __name__ == "__main__":
    unittest.main()
