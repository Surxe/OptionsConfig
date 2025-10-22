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


if __name__ == "__main__":
    unittest.main()
