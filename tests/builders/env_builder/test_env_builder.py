#!/usr/bin/env python3
"""Test script for EnvBuilder functionality"""

import sys
import unittest
import os
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
    """Test cases for EnvBuilder with direct parameters."""
    
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


class TestEnvBuilderWithToml(unittest.TestCase):
    """Test cases for EnvBuilder loading configuration from pyproject.toml."""
    
    def setUp(self):
        """Set up test environment and save current directory."""
        self.test_dir = Path(__file__).parent
        self.original_cwd = os.getcwd()
        self.env_example_path = self.test_dir / 'env_toml.example'
        
        # Ensure the test directory has pyproject.toml
        self.toml_path = self.test_dir / 'pyproject.toml'
        self.assertTrue(self.toml_path.exists(), 
                       "pyproject.toml must exist in test directory")
    
    def tearDown(self):
        """Restore original directory and clean up test files."""
        os.chdir(self.original_cwd)
        # Clean up generated test file
        if self.env_example_path.exists():
            self.env_example_path.unlink()
    
    def test_build_env_example_from_toml(self):
        """Test that EnvBuilder loads schema from pyproject.toml and generates correct content."""
        # Change to test directory where pyproject.toml is located
        os.chdir(self.test_dir)
        
        # Create EnvBuilder without passing schema - should load from pyproject.toml
        builder = EnvBuilder(env_example_path=self.env_example_path)
        builder.build()
        
        # Verify file was created
        self.assertTrue(self.env_example_path.exists(), 
                       "env.example file was not created")
        
        # Read generated content
        genned_content = self._read_env_file()
        
        # Verify expected content
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
        self.assertEqual(genned_content.strip(), expected_content.strip(), 
                        "Generated .env.example content does not match expected content when loaded from toml")
    
    def test_build_env_example_toml_no_path_param(self):
        """Test that EnvBuilder can generate with default path when only loading schema from toml."""
        # Change to test directory
        os.chdir(self.test_dir)
        
        # Use a custom default path for this test
        custom_path = self.test_dir / 'env_default.example'
        
        try:
            # Create builder with schema from toml, but specify path directly
            builder = EnvBuilder(env_example_path=custom_path)
            builder.build()
            
            # Verify file was created
            self.assertTrue(custom_path.exists(), 
                           "env.example file was not created at custom path")
            
            # Verify content is correct
            with open(custom_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertIn('SHOULD_PARSE', content, 
                             "Schema was not loaded correctly from toml")
                self.assertIn('GAME_TO_PARSE', content, 
                             "Schema was not loaded correctly from toml")
        
        finally:
            # Clean up
            if custom_path.exists():
                custom_path.unlink()
    
    def test_toml_schema_content_matches_direct_param(self):
        """Test that schema loaded from toml produces identical output to direct parameter."""
        os.chdir(self.test_dir)
        
        # Build with toml
        toml_path = self.test_dir / 'env_toml_test.example'
        builder_toml = EnvBuilder(env_example_path=toml_path)
        builder_toml.build()
        
        # Build with direct parameter
        direct_path = self.test_dir / 'env_direct_test.example'
        builder_direct = EnvBuilder(schema=OPTIONS_SCHEMA, env_example_path=direct_path)
        builder_direct.build()
        
        try:
            # Read both files
            with open(toml_path, 'r', encoding='utf-8') as f:
                toml_content = f.read()
            with open(direct_path, 'r', encoding='utf-8') as f:
                direct_content = f.read()
            
            # Should be identical
            self.assertEqual(toml_content, direct_content,
                           "Output from toml-loaded schema should match direct parameter schema")
        
        finally:
            # Clean up
            if toml_path.exists():
                toml_path.unlink()
            if direct_path.exists():
                direct_path.unlink()
    
    def _read_env_file(self):
        """Read generated .env.example file."""
        with open(self.env_example_path, 'r', encoding='utf-8') as f:
            return f.read()


if __name__ == "__main__":
    unittest.main()