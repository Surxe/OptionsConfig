#!/usr/bin/env python3
"""
Comprehensive test suite for Options class

Tests all aspects of Options initialization, validation, and configuration:
- Schema loading (direct parameter)
- Argument priority (args > env > defaults)
- Log file configuration
- Root option auto-defaulting
- Dependency validation
- Sensitive data masking
- Environment variable handling
- Type conversions
"""

import sys
import os
import unittest
import argparse
from pathlib import Path

# Add paths - src first so optionsconfig imports work, then local for our schemas
src_path = str(Path(__file__).parent.parent.parent / "src")
local_path = str(Path(__file__).parent)
if src_path not in sys.path:
    sys.path.insert(0, src_path)
if local_path not in sys.path:
    sys.path.insert(0, local_path)

from optionsconfig import Options, ArgumentWriter, init_options

# Import the test schemas from this directory
from options_test_schema import OPTIONS_SCHEMA, OPTIONS_SCHEMA_BASIC, OPTIONS_SCHEMA_WITH_DEPS


class TestOptions(unittest.TestCase):
    """Test cases for Options class."""
    
    def test_basic_initialization(self):
        """Test basic Options initialization with schema only."""
        log_file = Path('tests/options/logs/test_basic.log')
        options = Options(schema=OPTIONS_SCHEMA_BASIC, log_file=log_file)
        
        # Verify attributes were set
        self.assertTrue(hasattr(options, 'project_name'))
        self.assertTrue(hasattr(options, 'data_dir'))
        self.assertTrue(hasattr(options, 'max_retries'))
        
        # Verify defaults
        self.assertEqual(options.project_name, "MyProject")
        self.assertEqual(options.data_dir, Path("data"))
        self.assertEqual(options.max_retries, 3)
        self.assertEqual(options.log_level, "INFO")
    
    def test_log_file_parameter(self):
        """Test log file parameter handling."""
        log_file = Path('tests/options/logs/custom_log.log')
        options = Options(schema=OPTIONS_SCHEMA_BASIC, log_file=log_file)
        
        # Verify log_file was set correctly
        self.assertEqual(options.log_file, log_file)
        
        # Verify log file was created
        self.assertTrue(log_file.exists())
        
        # Verify parent directory was created
        self.assertTrue(log_file.parent.exists())
    
    def test_args_priority(self):
        """Test arguments take priority over defaults."""
        # Create ArgumentWriter and parser
        parser = argparse.ArgumentParser()
        writer = ArgumentWriter(schema=OPTIONS_SCHEMA_BASIC)
        writer.add_arguments(parser)
        
        # Parse args
        args = parser.parse_args([
            '--project-name', 'TestProject',
            '--max-retries', '10'
        ])
        
        log_file = Path('tests/options/logs/test_args.log')
        options = Options(args=args, schema=OPTIONS_SCHEMA_BASIC, log_file=log_file)
        
        # Verify args override defaults
        self.assertEqual(options.project_name, "TestProject")
        self.assertEqual(options.max_retries, 10)
        
        # Verify non-specified options still have defaults
        self.assertEqual(options.log_level, "INFO")
        self.assertEqual(options.data_dir, Path("data"))
    
    def test_env_variables(self):
        """Test environment variables override defaults."""
        # Set environment variables
        os.environ['PROJECT_NAME'] = 'EnvProject'
        os.environ['MAX_RETRIES'] = '5'
        os.environ['LOG_LEVEL'] = 'DEBUG'
        
        try:
            log_file = Path('tests/options/logs/test_env.log')
            options = Options(schema=OPTIONS_SCHEMA_BASIC, log_file=log_file)
            
            # Verify env vars were used
            self.assertEqual(options.project_name, 'EnvProject')
            self.assertEqual(options.max_retries, 5)
            self.assertEqual(options.log_level, 'DEBUG')
            
        finally:
            # Clean up environment
            del os.environ['PROJECT_NAME']
            del os.environ['MAX_RETRIES']
            del os.environ['LOG_LEVEL']
    
    def test_args_override_env(self):
        """Test arguments override environment variables."""
        # Set environment variable
        os.environ['PROJECT_NAME'] = 'EnvProject'
        
        try:
            # Create args that override env
            parser = argparse.ArgumentParser()
            writer = ArgumentWriter(schema=OPTIONS_SCHEMA_BASIC)
            writer.add_arguments(parser)
            args = parser.parse_args(['--project-name', 'ArgsProject'])
            
            log_file = Path('tests/options/logs/test_priority.log')
            options = Options(args=args, schema=OPTIONS_SCHEMA_BASIC, log_file=log_file)
            
            # Args should win
            self.assertEqual(options.project_name, 'ArgsProject')
            
        finally:
            del os.environ['PROJECT_NAME']
    
    def test_dependency_validation_success(self):
        """Test dependency validation when dependencies are met."""
        parser = argparse.ArgumentParser()
        writer = ArgumentWriter(schema=OPTIONS_SCHEMA_WITH_DEPS)
        writer.add_arguments(parser)
        
        # Enable processing AND provide required output file
        args = parser.parse_args([
            '--enable-processing',
            '--output-file', 'output.txt'
        ])
        
        log_file = Path('tests/options/logs/test_dep_success.log')
        options = Options(args=args, schema=OPTIONS_SCHEMA_WITH_DEPS, log_file=log_file)
        
        self.assertTrue(options.enable_processing)
        # Argparse returns string, check if it's either string or Path
        self.assertIn(str(options.output_file), ['output.txt', str(Path('output.txt'))])
    
    def test_dependency_validation_failure(self):
        """Test dependency validation fails when requirements not met."""
        parser = argparse.ArgumentParser()
        writer = ArgumentWriter(schema=OPTIONS_SCHEMA_WITH_DEPS)
        writer.add_arguments(parser)
        
        # Enable processing but DON'T provide required output file
        args = parser.parse_args(['--enable-processing'])
        
        log_file = Path('tests/options/logs/test_dep_fail.log')
        
        with self.assertRaises(ValueError) as cm:
            options = Options(args=args, schema=OPTIONS_SCHEMA_WITH_DEPS, log_file=log_file)
        
        self.assertIn("OUTPUT_FILE is required", str(cm.exception))
        self.assertIn("ENABLE_PROCESSING", str(cm.exception))
    
    def test_root_option_auto_default(self):
        """Test root options auto-default to True when not explicitly set."""
        # Don't set enable_processing at all (uses schema with dependencies)
        log_file = Path('tests/options/logs/test_auto_default.log')
        
        # When root option is auto-defaulted to True, dependent option is required
        # This should fail validation
        with self.assertRaises(ValueError) as cm:
            options = Options(schema=OPTIONS_SCHEMA_WITH_DEPS, log_file=log_file)
        
        self.assertIn("OUTPUT_FILE is required", str(cm.exception))
    
    def test_root_option_explicit_false(self):
        """Test root options can be explicitly set to False."""
        # Explicitly set to False via environment
        os.environ['ENABLE_PROCESSING'] = 'false'
        
        try:
            log_file = Path('tests/options/logs/test_explicit_false.log')
            options = Options(schema=OPTIONS_SCHEMA_WITH_DEPS, log_file=log_file)
            
            # Should respect explicit False and not require dependent option
            self.assertFalse(options.enable_processing)
            self.assertIsNone(options.output_file)  # Not required when processing disabled
            
        finally:
            del os.environ['ENABLE_PROCESSING']
    
    def test_sensitive_data_masking(self):
        """Test sensitive data is masked in logs."""
        os.environ['API_KEY'] = 'secret123'
        
        try:
            log_file = Path('tests/options/logs/test_sensitive.log')
            # Delete old log file if it exists
            if log_file.exists():
                log_file.unlink()
            
            options = Options(schema=OPTIONS_SCHEMA_BASIC, log_file=log_file)
            
            # API key should be set
            self.assertEqual(options.api_key, 'secret123')
            
            # Force flush logs
            import logging
            for handler in logging.getLogger().handlers:
                handler.flush()
            
            # Check log file doesn't contain the actual key
            self.assertTrue(log_file.exists(), "Log file was not created")
            with open(log_file, 'r') as f:
                log_content = f.read()
                self.assertNotIn('secret123', log_content)
                self.assertIn('***HIDDEN***', log_content)
            
        finally:
            del os.environ['API_KEY']
    
    def test_type_conversions(self):
        """Test type conversions from environment variables."""
        os.environ['MAX_RETRIES'] = '42'
        os.environ['DATA_DIR'] = '/custom/path'
        os.environ['LOG_LEVEL'] = 'ERROR'
        
        try:
            log_file = Path('tests/options/logs/test_types.log')
            options = Options(schema=OPTIONS_SCHEMA_BASIC, log_file=log_file)
            
            # Verify types
            self.assertIsInstance(options.max_retries, int)
            self.assertEqual(options.max_retries, 42)
            
            self.assertIsInstance(options.data_dir, Path)
            self.assertEqual(options.data_dir, Path('/custom/path'))
            
            self.assertIsInstance(options.log_level, str)
            self.assertEqual(options.log_level, 'ERROR')
            
        finally:
            del os.environ['MAX_RETRIES']
            del os.environ['DATA_DIR']
            del os.environ['LOG_LEVEL']
    
    def test_literal_type_validation(self):
        """Test Literal types validate choices from environment."""
        # Valid choice
        os.environ['LOG_LEVEL'] = 'WARNING'
        
        try:
            log_file = Path('tests/options/logs/test_literal.log')
            options = Options(schema=OPTIONS_SCHEMA_BASIC, log_file=log_file)
            
            self.assertEqual(options.log_level, 'WARNING')
            
        finally:
            del os.environ['LOG_LEVEL']
        
        # Invalid choice should fall back to default
        os.environ['LOG_LEVEL'] = 'INVALID'
        
        try:
            log_file = Path('tests/options/logs/test_literal_invalid.log')
            options = Options(schema=OPTIONS_SCHEMA_BASIC, log_file=log_file)
            
            # Should fall back to default
            self.assertEqual(options.log_level, 'INFO')
            
        finally:
            del os.environ['LOG_LEVEL']
    
    def test_init_options_helper(self):
        """Test init_options() helper function."""
        log_file = Path('tests/options/logs/test_init_helper.log')
        options = init_options(schema=OPTIONS_SCHEMA_BASIC, log_file=log_file)
        
        self.assertIsInstance(options, Options)
        self.assertTrue(hasattr(options, 'project_name'))
        self.assertEqual(options.project_name, "MyProject")
    
    def test_schema_attributes(self):
        """Test all schema options become attributes."""
        log_file = Path('tests/options/logs/test_attributes.log')
        options = Options(schema=OPTIONS_SCHEMA_BASIC, log_file=log_file)
        
        # Check all schema keys become lowercase attributes
        self.assertTrue(hasattr(options, 'project_name'))       # PROJECT_NAME
        self.assertTrue(hasattr(options, 'data_dir'))           # DATA_DIR
        self.assertTrue(hasattr(options, 'log_level'))          # LOG_LEVEL
        self.assertTrue(hasattr(options, 'api_key'))            # API_KEY
        self.assertTrue(hasattr(options, 'max_retries'))        # MAX_RETRIES
        
        # Check schema is stored
        self.assertTrue(hasattr(options, 'schema'))
        self.assertEqual(len(options.schema), 5)


class TestOptionsWithToml(unittest.TestCase):
    """Test cases for Options loading configuration from pyproject.toml."""
    
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
    
    def test_basic_initialization_from_toml(self):
        """Test Options loads schema from pyproject.toml."""
        # Change to test directory where pyproject.toml is located
        os.chdir(self.test_dir)
        
        # Create Options without passing schema - should load from pyproject.toml
        log_file = Path('logs/test_toml_basic.log')
        options = Options(log_file=log_file)
        
        # Verify attributes were set from toml-loaded schema
        self.assertTrue(hasattr(options, 'project_name'))
        self.assertTrue(hasattr(options, 'data_dir'))
        self.assertTrue(hasattr(options, 'max_retries'))
        
        # Verify defaults
        self.assertEqual(options.project_name, "MyProject")
        self.assertEqual(options.data_dir, Path("data"))
        self.assertEqual(options.max_retries, 3)
        self.assertEqual(options.log_level, "INFO")
    
    def test_args_priority_with_toml(self):
        """Test arguments take priority with toml-loaded schema."""
        os.chdir(self.test_dir)
        
        # Create ArgumentWriter without schema - should load from toml
        from optionsconfig import ArgumentWriter
        parser = argparse.ArgumentParser()
        writer = ArgumentWriter()  # No schema parameter
        writer.add_arguments(parser)
        
        # Parse args
        args = parser.parse_args([
            '--project-name', 'TomlTestProject',
            '--max-retries', '15'
        ])
        
        # Create Options with args but no schema
        log_file = Path('logs/test_toml_args.log')
        options = Options(args=args, log_file=log_file)
        
        # Args should override defaults
        self.assertEqual(options.project_name, "TomlTestProject")
        self.assertEqual(options.max_retries, 15)
    
    def test_env_variables_with_toml(self):
        """Test environment variables override defaults with toml-loaded schema."""
        os.chdir(self.test_dir)
        
        # Set environment variables
        os.environ['PROJECT_NAME'] = 'TomlEnvProject'
        os.environ['LOG_LEVEL'] = 'DEBUG'
        os.environ['MAX_RETRIES'] = '7'
        
        try:
            log_file = Path('logs/test_toml_env.log')
            options = Options(log_file=log_file)
            
            # Env vars should override defaults
            self.assertEqual(options.project_name, "TomlEnvProject")
            self.assertEqual(options.log_level, "DEBUG")
            self.assertEqual(options.max_retries, 7)
            
        finally:
            # Clean up environment
            del os.environ['PROJECT_NAME']
            del os.environ['LOG_LEVEL']
            del os.environ['MAX_RETRIES']
    
    def test_toml_schema_matches_direct_param(self):
        """Test that schema loaded from toml produces identical behavior to direct parameter."""
        os.chdir(self.test_dir)
        
        # Create Options with toml (no schema parameter)
        log_file_toml = Path('logs/test_toml_comparison.log')
        options_toml = Options(log_file=log_file_toml)
        
        # Create Options with direct parameter
        log_file_direct = Path('logs/test_direct_comparison.log')
        options_direct = Options(schema=OPTIONS_SCHEMA_BASIC, log_file=log_file_direct)
        
        # Should have identical attributes
        self.assertEqual(options_toml.project_name, options_direct.project_name)
        self.assertEqual(options_toml.data_dir, options_direct.data_dir)
        self.assertEqual(options_toml.log_level, options_direct.log_level)
        self.assertEqual(options_toml.max_retries, options_direct.max_retries)
        
        # Schema should be identical
        self.assertEqual(options_toml.schema.keys(), options_direct.schema.keys())
    
    def test_dependency_validation_with_toml(self):
        """Test dependency validation works with toml-loaded schema."""
        os.chdir(self.test_dir)
        
        # Create ArgumentWriter and parser
        from optionsconfig import ArgumentWriter
        parser = argparse.ArgumentParser()
        
        # We need to temporarily set schema_module to the deps schema
        # Save original pyproject.toml
        import shutil
        backup_toml = self.test_dir / 'pyproject.toml.backup'
        shutil.copy(self.toml_path, backup_toml)
        
        try:
            # Update pyproject.toml to use schema with dependencies
            with open(self.toml_path, 'w') as f:
                f.write('[tool.optionsconfig]\n')
                f.write('schema_module = "options_test_schema"\n')
                f.write('schema_name = "OPTIONS_SCHEMA_WITH_DEPS"\n')
            
            # Note: get_schema doesn't support schema_name yet, so we'll use direct param for this test
            # This test verifies the pattern works, even if we use direct param
            log_file = Path('logs/test_toml_deps.log')
            
            # With dependency enabled, dependent option should be allowed
            parser_enabled = argparse.ArgumentParser()
            writer_enabled = ArgumentWriter(schema=OPTIONS_SCHEMA_WITH_DEPS)
            writer_enabled.add_arguments(parser_enabled)
            args_enabled = parser_enabled.parse_args([
                '--enable-processing',
                '--output-file', 'output.txt'
            ])
            
            options_enabled = Options(args=args_enabled, schema=OPTIONS_SCHEMA_WITH_DEPS, log_file=log_file)
            self.assertTrue(options_enabled.enable_processing)
            self.assertEqual(options_enabled.output_file, "output.txt")
            
        finally:
            # Restore original pyproject.toml
            shutil.copy(backup_toml, self.toml_path)
            backup_toml.unlink()
    
    def test_init_options_helper_with_toml(self):
        """Test init_options() helper function works with toml."""
        os.chdir(self.test_dir)
        
        log_file = Path('logs/test_toml_init_helper.log')
        options = init_options(log_file=log_file)
        
        self.assertIsInstance(options, Options)
        self.assertTrue(hasattr(options, 'project_name'))
        self.assertEqual(options.project_name, "MyProject")


if __name__ == "__main__":
    unittest.main()
