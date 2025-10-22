#!/usr/bin/env python3
"""Test script for both builders"""

import sys
import unittest
from pathlib import Path
import os

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


class TestBothBuildersWithToml(unittest.TestCase):
    """Test cases for both builders loading schema from pyproject.toml."""
    
    def setUp(self):
        """Set up test environment and save current directory."""
        self.test_dir = Path(__file__).parent
        self.original_cwd = os.getcwd()
        
        # Ensure the test directory has pyproject.toml
        self.toml_path = self.test_dir / 'pyproject.toml'
        self.assertTrue(self.toml_path.exists(), 
                       "pyproject.toml must exist in test directory")
        
        # Set up relative paths from test directory
        self.env_path = Path('test_both_toml.env.example')
        self.readme_path = Path('test_both_toml_README.md')
    
    def tearDown(self):
        """Restore original directory and clean up test files."""
        os.chdir(self.original_cwd)
        
        # Clean up test files
        for path in [self.test_dir / self.env_path, self.test_dir / self.readme_path]:
            if path.exists():
                path.unlink()
    
    def test_both_builders_from_toml(self):
        """Test both builders loading schema from pyproject.toml."""
        os.chdir(self.test_dir)
        sys.path.insert(0, str(self.test_dir))
        
        try:
            # Create a test README with markers
            test_readme_content = """# Test README

<!-- BEGIN_GENERATED_OPTIONS -->
<!-- END_GENERATED_OPTIONS -->
"""
            
            with open(self.readme_path, 'w', encoding='utf-8') as f:
                f.write(test_readme_content)
            
            # Test EnvBuilder without explicit schema
            env_builder = EnvBuilder(env_example_path=self.env_path)
            result = env_builder.build()
            self.assertTrue(result, "EnvBuilder failed")
            
            # Test ReadmeBuilder without explicit schema
            readme_builder = ReadmeBuilder(readme_path=self.readme_path)
            result = readme_builder.build()
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
                
        finally:
            if str(self.test_dir) in sys.path:
                sys.path.remove(str(self.test_dir))
    
    def test_both_builders_using_toml_paths(self):
        """Test that builders can use paths from pyproject.toml."""
        os.chdir(self.test_dir)
        sys.path.insert(0, str(self.test_dir))
        
        try:
            # Use paths from pyproject.toml (test_toml.env.example and test_toml_README.md)
            toml_env_path = Path('test_toml.env.example')
            toml_readme_path = Path('test_toml_README.md')
            
            # Create a test README with markers
            test_readme_content = """# Test README from TOML

<!-- BEGIN_GENERATED_OPTIONS -->
<!-- END_GENERATED_OPTIONS -->
"""
            
            with open(toml_readme_path, 'w', encoding='utf-8') as f:
                f.write(test_readme_content)
            
            # Test builders loading both schema and paths from toml
            env_builder = EnvBuilder()  # Should use toml schema and path
            readme_builder = ReadmeBuilder()  # Should use toml schema and path
            
            # Build both
            env_result = env_builder.build()
            readme_result = readme_builder.build()
            
            self.assertTrue(env_result, "EnvBuilder with toml paths failed")
            self.assertTrue(readme_result, "ReadmeBuilder with toml paths failed")
            
            # Verify files exist
            self.assertTrue(toml_env_path.exists(), "env.example from toml not created")
            self.assertTrue(toml_readme_path.exists(), "README from toml not created")
            
            # Clean up toml-path files
            if toml_env_path.exists():
                toml_env_path.unlink()
            if toml_readme_path.exists():
                toml_readme_path.unlink()
                
        finally:
            if str(self.test_dir) in sys.path:
                sys.path.remove(str(self.test_dir))
    
    def test_direct_params_override_toml(self):
        """Test that direct parameters override pyproject.toml configuration."""
        os.chdir(self.test_dir)
        sys.path.insert(0, str(self.test_dir))
        
        try:
            # Create custom schema
            custom_schema = {
                "CUSTOM_VAR": {
                    "env": "CUSTOM_VAR",
                    "arg": "--custom-var",
                    "type": str,
                    "default": "custom",
                    "section": "Custom",
                    "help": "Custom variable"
                }
            }
            
            custom_env_path = Path('test_custom.env.example')
            custom_readme_path = Path('test_custom_README.md')
            
            # Create a test README with markers
            test_readme_content = """# Custom README

<!-- BEGIN_GENERATED_OPTIONS -->
<!-- END_GENERATED_OPTIONS -->
"""
            
            with open(custom_readme_path, 'w', encoding='utf-8') as f:
                f.write(test_readme_content)
            
            # Create builders with explicit parameters
            env_builder = EnvBuilder(schema=custom_schema, env_example_path=custom_env_path)
            readme_builder = ReadmeBuilder(schema=custom_schema, readme_path=custom_readme_path)
            
            # Build
            env_builder.build()
            readme_builder.build()
            
            # Verify custom schema was used (not integration_schema from toml)
            with open(custom_env_path, 'r', encoding='utf-8') as f:
                env_content = f.read()
                self.assertIn('CUSTOM_VAR', env_content)
                self.assertNotIn('SHOULD_PARSE', env_content)
            
            with open(custom_readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()
                self.assertIn('**CUSTOM_VAR**', readme_content)
                self.assertNotIn('**SHOULD_PARSE**', readme_content)
            
            # Clean up
            if custom_env_path.exists():
                custom_env_path.unlink()
            if custom_readme_path.exists():
                custom_readme_path.unlink()
                
        finally:
            if str(self.test_dir) in sys.path:
                sys.path.remove(str(self.test_dir))


if __name__ == "__main__":
    unittest.main()