#!/usr/bin/env python3
"""Test script for ReadmeBuilder functionality"""

import sys
from pathlib import Path

# Add src to path for local testing
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

from optionsconfig.builders.readme_builder import ReadmeBuilder

# Import the test schema from this directory
from options_schema import OPTIONS_SCHEMA

def test(readme_path: Path):
    # Create a test README with markers
    test_readme_content = """# Test README

Some content here.

<!-- BEGIN_GENERATED_OPTIONS -->
Old content to be replaced
<!-- END_GENERATED_OPTIONS -->

More content after.
"""
    
    # Write test README
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(test_readme_content)
    
    # Pass the schema directly and build
    ReadmeBuilder(schema=OPTIONS_SCHEMA, readme_path=readme_path).build()
    
    # Read generated README
    with open(readme_path, 'r', encoding='utf-8') as f:
        genned_content = f.read()
    
    # Check that markers are present
    assert "<!-- BEGIN_GENERATED_OPTIONS -->" in genned_content, "Start marker not found"
    assert "<!-- END_GENERATED_OPTIONS -->" in genned_content, "End marker not found"
    
    # Check that options are documented
    assert "**SHOULD_PARSE**" in genned_content, "SHOULD_PARSE option not found"
    assert "**GAME_TO_PARSE**" in genned_content, "GAME_TO_PARSE option not found"
    assert "#### Parse" in genned_content, "Parse section not found"
    
    # Check that old content was replaced
    assert "Old content to be replaced" not in genned_content, "Old content was not replaced"
    
    # Check that surrounding content is preserved
    assert "Some content here." in genned_content, "Content before markers was lost"
    assert "More content after." in genned_content, "Content after markers was lost"
    
    print("Generated README content validated successfully!")

if __name__ == "__main__":
    readme_path = Path('tests/builders/readme_builder/TEST_README.md')
    test(readme_path)
    print("All tests completed!")
