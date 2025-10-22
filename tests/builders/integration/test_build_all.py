#!/usr/bin/env python3
"""Simple test for build_all.py"""

import sys
from pathlib import Path

# Add src to path for local testing
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

from optionsconfig.builders import EnvBuilder, ReadmeBuilder

# Import the test schema from this directory
from options_schema import OPTIONS_SCHEMA

def test_build_all():
    """Test that both builders work together."""
    
    # Setup paths
    env_path = Path('tests/builders/integration/test_all.env.example')
    readme_path = Path('tests/builders/integration/test_all_README.md')
    
    # Create a test README with markers
    test_readme_content = """# Test README
<!-- BEGIN_GENERATED_OPTIONS -->
<!-- END_GENERATED_OPTIONS -->
"""
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(test_readme_content)
    
    # Build both
    env_result = EnvBuilder(schema=OPTIONS_SCHEMA, env_example_path=env_path).build()
    readme_result = ReadmeBuilder(schema=OPTIONS_SCHEMA, readme_path=readme_path).build()
    
    # Verify
    assert env_result and readme_result, "One or both builders failed"
    assert env_path.exists() and readme_path.exists(), "Files not created"
    
    print("✓ Both builders completed successfully")

if __name__ == "__main__":
    test_build_all()
    print("All tests completed!")
