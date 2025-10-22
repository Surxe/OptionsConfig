#!/usr/bin/env python3
"""Test script for ReadmeBuilder functionality"""

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

from optionsconfig.builders.readme_builder import ReadmeBuilder
from readme_builder_schema import OPTIONS_SCHEMA


class TestReadmeBuilder(unittest.TestCase):
    """Test cases for ReadmeBuilder."""
    
    def setUp(self):
        """Set up test file path."""
        self.readme_path = Path('tests/builders/readme_builder/TEST_README.md')
    
    def test_build_readme(self):
        """Test that ReadmeBuilder generates correct README content."""
        # Create a test README with markers
        test_readme_content = """# Test README

Some content here.

<!-- BEGIN_GENERATED_OPTIONS -->
Old content to be replaced
<!-- END_GENERATED_OPTIONS -->

More content after.
"""
        
        # Write test README
        with open(self.readme_path, 'w', encoding='utf-8') as f:
            f.write(test_readme_content)
        
        # Pass the schema directly and build
        ReadmeBuilder(schema=OPTIONS_SCHEMA, readme_path=self.readme_path).build()
        
        # Read generated README
        with open(self.readme_path, 'r', encoding='utf-8') as f:
            genned_content = f.read()
        
        # Check that markers are present
        self.assertIn("<!-- BEGIN_GENERATED_OPTIONS -->", genned_content, "Start marker not found")
        self.assertIn("<!-- END_GENERATED_OPTIONS -->", genned_content, "End marker not found")
        
        # Check that options are documented
        self.assertIn("**SHOULD_PARSE**", genned_content, "SHOULD_PARSE option not found")
        self.assertIn("**GAME_TO_PARSE**", genned_content, "GAME_TO_PARSE option not found")
        self.assertIn("#### Parse", genned_content, "Parse section not found")
        
        # Check that old content was replaced
        self.assertNotIn("Old content to be replaced", genned_content, "Old content was not replaced")
        
        # Check that surrounding content is preserved
        self.assertIn("Some content here.", genned_content, "Content before markers was lost")
        self.assertIn("More content after.", genned_content, "Content after markers was lost")


if __name__ == "__main__":
    unittest.main()
