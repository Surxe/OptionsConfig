#!/usr/bin/env python3
"""Test script for both builders"""

import sys
from pathlib import Path

# Add src to path for local testing
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

from optionsconfig.builders import EnvBuilder, ReadmeBuilder

# Import the test schema from this directory
from options_schema import OPTIONS_SCHEMA

def test_both_builders():
    """Test both EnvBuilder and ReadmeBuilder together."""
    
    # Setup paths
    env_path = Path('tests/builders/integration/test_both.env.example')
    readme_path = Path('tests/builders/integration/test_both_README.md')
    
    # Create a test README with markers
    test_readme_content = """# Test README

<!-- BEGIN_GENERATED_OPTIONS -->
<!-- END_GENERATED_OPTIONS -->
"""
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(test_readme_content)
    
    print("=" * 60)
    print("Testing EnvBuilder...")
    print("=" * 60)
    result = EnvBuilder(schema=OPTIONS_SCHEMA, env_example_path=env_path).build()
    assert result, "EnvBuilder failed"
    print()
    
    print("=" * 60)
    print("Testing ReadmeBuilder...")
    print("=" * 60)
    result = ReadmeBuilder(schema=OPTIONS_SCHEMA, readme_path=readme_path).build()
    assert result, "ReadmeBuilder failed"
    print()
    
    # Verify both files exist
    assert env_path.exists(), "env.example was not created"
    assert readme_path.exists(), "README.md was not created"
    
    # Verify content
    with open(env_path, 'r', encoding='utf-8') as f:
        env_content = f.read()
        assert 'SHOULD_PARSE' in env_content, "SHOULD_PARSE not in env.example"
        assert 'GAME_TO_PARSE' in env_content, "GAME_TO_PARSE not in env.example"
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme_content = f.read()
        assert '**SHOULD_PARSE**' in readme_content, "SHOULD_PARSE not in README"
        assert '**GAME_TO_PARSE**' in readme_content, "GAME_TO_PARSE not in README"
    
    print("=" * 60)
    print("✓ All validations passed!")
    print("=" * 60)
    print(f"Generated files:")
    print(f"  - {env_path}")
    print(f"  - {readme_path}")

if __name__ == "__main__":
    test_both_builders()
    print("\nAll tests completed successfully!")
