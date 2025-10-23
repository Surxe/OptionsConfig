#!/usr/bin/env python3
"""Basic test suite for schema.py module."""

import sys
import os
import unittest
from pathlib import Path
import tempfile
import shutil

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from optionsconfig.schema import get_schema, _load_schema_from_config, OptionDefinition


class TestSchema(unittest.TestCase):
    """Test cases for schema.py module."""
    
    def test_get_schema_with_direct_param(self):
        """Test get_schema() with direct schema parameter."""
        test_schema = {
            "TEST_OPTION": {
                "env": "TEST_OPTION",
                "arg": "--test-option",
                "type": str,
                "default": "test",
                "section": "Test",
                "help": "Test option"
            }
        }
        
        result = get_schema(schema=test_schema)
        
        self.assertEqual(result, test_schema)
        self.assertIn("TEST_OPTION", result)
        self.assertEqual(result["TEST_OPTION"]["default"], "test")
    
    def test_get_schema_without_param_no_config(self):
        """Test get_schema() without parameter and no config file."""
        original_dir = os.getcwd()
        tmpdir = None
        
        try:
            tmpdir = tempfile.mkdtemp()
            os.chdir(tmpdir)
            
            # Should raise ImportError
            with self.assertRaises(ImportError) as cm:
                get_schema()
            
            self.assertIn("No OPTIONS_SCHEMA found", str(cm.exception))
        finally:
            os.chdir(original_dir)
            if tmpdir:
                shutil.rmtree(tmpdir, ignore_errors=True)
    
    def test_load_schema_from_config_no_file(self):
        """Test _load_schema_from_config() with no pyproject.toml."""
        original_dir = os.getcwd()
        tmpdir = None
        
        try:
            tmpdir = tempfile.mkdtemp()
            os.chdir(tmpdir)
            
            result = _load_schema_from_config()
            
            self.assertIsNone(result)
        finally:
            os.chdir(original_dir)
            if tmpdir:
                shutil.rmtree(tmpdir, ignore_errors=True)
    
    def test_option_definition_typed_dict(self):
        """Test OptionDefinition TypedDict structure."""
        # Create a valid OptionDefinition
        option: OptionDefinition = {
            "env": "TEST_VAR",
            "arg": "--test-var",
            "type": str,
            "default": "value",
            "section": "Test",
            "help": "Test help text",
            "depends_on": ["OTHER_OPTION"],
            "sensitive": False
        }
        
        # Verify all fields are accessible
        self.assertEqual(option["env"], "TEST_VAR")
        self.assertEqual(option["arg"], "--test-var")
        self.assertEqual(option["type"], str)
        self.assertEqual(option["default"], "value")
        self.assertEqual(option["section"], "Test")
        self.assertEqual(option["help"], "Test help text")
        self.assertEqual(option["depends_on"], ["OTHER_OPTION"])
        self.assertFalse(option["sensitive"])
    
    def test_existing_sample_schema(self):
        """Test loading existing sample_schema.py from tests/schema/."""
        schema_dir = Path(__file__).parent
        sys.path.insert(0, str(schema_dir))
        
        try:
            from sample_schema import OPTIONS_SCHEMA
            
            self.assertIsNotNone(OPTIONS_SCHEMA)
            self.assertIsInstance(OPTIONS_SCHEMA, dict)
            self.assertIn("SHOULD_PARSE", OPTIONS_SCHEMA)
            self.assertIn("GAME_NAME", OPTIONS_SCHEMA)
            
            # Test get_schema with it
            result = get_schema(schema=OPTIONS_SCHEMA)
            self.assertEqual(result, OPTIONS_SCHEMA)
        finally:
            sys.path.remove(str(schema_dir))


class TestSchemaWithToml(unittest.TestCase):
    """Test cases for schema loading from pyproject.toml."""
    
    def setUp(self):
        """Set up test environment and save current directory."""
        self.test_dir = Path(__file__).parent
        self.original_cwd = os.getcwd()
        
        # Ensure the test directory has pyproject.toml
        self.toml_path = self.test_dir / 'pyproject.toml'
        self.assertTrue(self.toml_path.exists(), 
                       "pyproject.toml must exist in test directory")
    
    def tearDown(self):
        """Restore original directory."""
        os.chdir(self.original_cwd)
    
    def test_load_schema_from_config_with_file(self):
        """Test _load_schema_from_config() successfully loads from pyproject.toml."""
        # Change to test directory where pyproject.toml is located
        os.chdir(self.test_dir)
        
        # Add test directory to path so schema module can be imported
        sys.path.insert(0, str(self.test_dir))
        
        try:
            result = _load_schema_from_config()
            
            self.assertIsNotNone(result)
            self.assertIsInstance(result, dict)
            self.assertIn("SHOULD_PARSE", result)
            self.assertIn("GAME_NAME", result)
        finally:
            sys.path.remove(str(self.test_dir))
    
    def test_get_schema_from_toml(self):
        """Test get_schema() loads from pyproject.toml when no parameter given."""
        os.chdir(self.test_dir)
        
        # Add test directory to path
        sys.path.insert(0, str(self.test_dir))
        
        try:
            result = get_schema()
            
            self.assertIsNotNone(result)
            self.assertIsInstance(result, dict)
            self.assertIn("SHOULD_PARSE", result)
            self.assertIn("GAME_NAME", result)
            
            # Verify it's the sample schema
            self.assertEqual(result["SHOULD_PARSE"]["env"], "SHOULD_PARSE")
            self.assertEqual(result["SHOULD_PARSE"]["type"], bool)
            
        finally:
            sys.path.remove(str(self.test_dir))
    
    def test_get_schema_direct_param_overrides_toml(self):
        """Test that direct parameter takes priority over pyproject.toml."""
        os.chdir(self.test_dir)
        
        # Add test directory to path
        sys.path.insert(0, str(self.test_dir))
        
        try:
            # Create a different schema
            override_schema = {
                "OVERRIDE_OPTION": {
                    "env": "OVERRIDE_OPTION",
                    "arg": "--override",
                    "type": str,
                    "default": "override",
                    "section": "Override",
                    "help": "Override option"
                }
            }
            
            result = get_schema(schema=override_schema)
            
            # Should get the direct parameter, not from toml
            self.assertEqual(result, override_schema)
            self.assertIn("OVERRIDE_OPTION", result)
            self.assertNotIn("SHOULD_PARSE", result)
            
        finally:
            sys.path.remove(str(self.test_dir))
    
    def test_toml_config_missing_schema_module(self):
        """Test that missing schema_module in toml returns None."""
        # Create a temp directory with invalid pyproject.toml
        tmpdir = tempfile.mkdtemp()
        original_dir = os.getcwd()
        
        try:
            os.chdir(tmpdir)
            
            # Create pyproject.toml without schema_module
            toml_path = Path(tmpdir) / 'pyproject.toml'
            with open(toml_path, 'w') as f:
                f.write('[tool.optionsconfig]\n')
                f.write('# No schema_module\n')
            
            result = _load_schema_from_config()
            
            self.assertIsNone(result)
            
        finally:
            os.chdir(original_dir)
            shutil.rmtree(tmpdir, ignore_errors=True)
    
    def test_toml_config_invalid_schema_module(self):
        """Test that invalid schema_module name returns None."""
        tmpdir = tempfile.mkdtemp()
        original_dir = os.getcwd()
        
        try:
            os.chdir(tmpdir)
            
            # Create pyproject.toml with non-existent module
            toml_path = Path(tmpdir) / 'pyproject.toml'
            with open(toml_path, 'w') as f:
                f.write('[tool.optionsconfig]\n')
                f.write('schema_module = "nonexistent_module_12345"\n')
            
            with self.assertRaises(ImportError):
                _load_schema_from_config()
            
        finally:
            os.chdir(original_dir)
            shutil.rmtree(tmpdir, ignore_errors=True)
    
    def test_toml_schema_matches_direct_import(self):
        """Test that toml-loaded schema matches directly imported schema."""
        os.chdir(self.test_dir)
        
        # Add test directory to path
        sys.path.insert(0, str(self.test_dir))
        
        try:
            # Load from toml
            toml_schema = get_schema()
            
            # Load directly
            from sample_schema import OPTIONS_SCHEMA
            direct_schema = get_schema(schema=OPTIONS_SCHEMA)
            
            # Should be identical
            self.assertEqual(toml_schema, direct_schema)
            self.assertEqual(toml_schema.keys(), direct_schema.keys())
            
            # Verify same content
            for key in toml_schema:
                self.assertEqual(toml_schema[key], direct_schema[key])
            
        finally:
            sys.path.remove(str(self.test_dir))


if __name__ == "__main__":
    unittest.main()
