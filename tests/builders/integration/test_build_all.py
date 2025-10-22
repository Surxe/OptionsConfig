#!/usr/bin/env python3
"""Simple test for build_all.py"""

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


class TestBuildAll(unittest.TestCase):
    """Test cases for building all documentation."""
    
    def setUp(self):
        """Set up test file paths."""
        self.env_path = Path('tests/builders/integration/test_all.env.example')
        self.readme_path = Path('tests/builders/integration/test_all_README.md')
    
    def test_build_all(self):
        """Test that both builders work together."""
        # Create a test README with markers
        test_readme_content = """# Test README
<!-- BEGIN_GENERATED_OPTIONS -->
<!-- END_GENERATED_OPTIONS -->
"""
        with open(self.readme_path, 'w', encoding='utf-8') as f:
            f.write(test_readme_content)
        
        # Build both
        env_result = EnvBuilder(schema=OPTIONS_SCHEMA, env_example_path=self.env_path).build()
        readme_result = ReadmeBuilder(schema=OPTIONS_SCHEMA, readme_path=self.readme_path).build()
        
        # Verify
        self.assertTrue(env_result and readme_result, "One or both builders failed")
        self.assertTrue(self.env_path.exists() and self.readme_path.exists(), "Files not created")


if __name__ == "__main__":
    unittest.main()
