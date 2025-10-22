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
import argparse
from pathlib import Path

# Add src to path for local testing
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

from optionsconfig import Options, ArgumentWriter

# Import the test schemas from this directory
from options_schema import OPTIONS_SCHEMA, OPTIONS_SCHEMA_BASIC, OPTIONS_SCHEMA_WITH_DEPS


def test_basic_initialization():
    """Test 1: Basic Options initialization with schema only."""
    print("=" * 60)
    print("Test 1: Basic Initialization")
    print("=" * 60)
    
    log_file = Path('tests/core/options/logs/test_basic.log')
    options = Options(schema=OPTIONS_SCHEMA_BASIC, log_file=log_file)
    
    # Verify attributes were set
    assert hasattr(options, 'project_name')
    assert hasattr(options, 'data_dir')
    assert hasattr(options, 'max_retries')
    
    # Verify defaults
    assert options.project_name == "MyProject"
    assert options.data_dir == Path("data")
    assert options.max_retries == 3
    assert options.log_level == "INFO"
    
    print("[PASS] Options initialized with schema")
    print(f"[PASS] Project name: {options.project_name}")
    print(f"[PASS] Data dir: {options.data_dir}")
    print(f"[PASS] Max retries: {options.max_retries}")
    print()


def test_log_file_parameter():
    """Test 2: Log file parameter handling."""
    print("=" * 60)
    print("Test 2: Log File Parameter")
    print("=" * 60)
    
    log_file = Path('tests/core/options/logs/custom_log.log')
    options = Options(schema=OPTIONS_SCHEMA_BASIC, log_file=log_file)
    
    # Verify log_file was set correctly
    assert options.log_file == log_file
    
    # Verify log file was created
    assert log_file.exists()
    
    # Verify parent directory was created
    assert log_file.parent.exists()
    
    print(f"[PASS] Log file set to: {options.log_file}")
    print("[PASS] Log file created successfully")
    print()


def test_args_priority():
    """Test 3: Arguments take priority over defaults."""
    print("=" * 60)
    print("Test 3: Argument Priority")
    print("=" * 60)
    
    # Create ArgumentWriter and parser
    parser = argparse.ArgumentParser()
    writer = ArgumentWriter(schema=OPTIONS_SCHEMA_BASIC)
    writer.add_arguments(parser)
    
    # Parse args
    args = parser.parse_args([
        '--project-name', 'TestProject',
        '--max-retries', '10'
    ])
    
    log_file = Path('tests/core/options/logs/test_args.log')
    options = Options(args=args, schema=OPTIONS_SCHEMA_BASIC, log_file=log_file)
    
    # Verify args override defaults
    assert options.project_name == "TestProject"
    assert options.max_retries == 10
    
    # Verify non-specified options still have defaults
    assert options.log_level == "INFO"
    assert options.data_dir == Path("data")
    
    print("[PASS] project_name from args: TestProject")
    print("[PASS] max_retries from args: 10")
    print("[PASS] log_level from default: INFO")
    print("[PASS] data_dir from default: data")
    print()


def test_env_variables():
    """Test 4: Environment variables override defaults."""
    print("=" * 60)
    print("Test 4: Environment Variable Priority")
    print("=" * 60)
    
    # Set environment variables
    os.environ['PROJECT_NAME'] = 'EnvProject'
    os.environ['MAX_RETRIES'] = '5'
    os.environ['LOG_LEVEL'] = 'DEBUG'
    
    try:
        log_file = Path('tests/core/options/logs/test_env.log')
        options = Options(schema=OPTIONS_SCHEMA_BASIC, log_file=log_file)
        
        # Verify env vars were used
        assert options.project_name == 'EnvProject'
        assert options.max_retries == 5
        assert options.log_level == 'DEBUG'
        
        print("[PASS] project_name from env: EnvProject")
        print("[PASS] max_retries from env: 5 (converted to int)")
        print("[PASS] log_level from env: DEBUG")
        print()
        
    finally:
        # Clean up environment
        del os.environ['PROJECT_NAME']
        del os.environ['MAX_RETRIES']
        del os.environ['LOG_LEVEL']


def test_args_override_env():
    """Test 5: Arguments override environment variables."""
    print("=" * 60)
    print("Test 5: Args Override Env Variables")
    print("=" * 60)
    
    # Set environment variable
    os.environ['PROJECT_NAME'] = 'EnvProject'
    
    try:
        # Create args that override env
        parser = argparse.ArgumentParser()
        writer = ArgumentWriter(schema=OPTIONS_SCHEMA_BASIC)
        writer.add_arguments(parser)
        args = parser.parse_args(['--project-name', 'ArgsProject'])
        
        log_file = Path('tests/core/options/logs/test_priority.log')
        options = Options(args=args, schema=OPTIONS_SCHEMA_BASIC, log_file=log_file)
        
        # Args should win
        assert options.project_name == 'ArgsProject'
        
        print("[PASS] Env var set to: EnvProject")
        print("[PASS] Args override to: ArgsProject")
        print("[PASS] Final value: ArgsProject")
        print()
        
    finally:
        del os.environ['PROJECT_NAME']


def test_dependency_validation_success():
    """Test 6: Dependency validation when dependencies are met."""
    print("=" * 60)
    print("Test 6: Dependency Validation (Success)")
    print("=" * 60)
    
    parser = argparse.ArgumentParser()
    writer = ArgumentWriter(schema=OPTIONS_SCHEMA_WITH_DEPS)
    writer.add_arguments(parser)
    
    # Enable processing AND provide required output file
    args = parser.parse_args([
        '--enable-processing',
        '--output-file', 'output.txt'
    ])
    
    log_file = Path('tests/core/options/logs/test_dep_success.log')
    options = Options(args=args, schema=OPTIONS_SCHEMA_WITH_DEPS, log_file=log_file)
    
    assert options.enable_processing is True
    # Argparse returns string, Options converts to Path for Path types from env
    # but args come through as-is, so check if it's either string or Path
    assert str(options.output_file) == 'output.txt' or options.output_file == Path('output.txt')
    
    print("[PASS] Dependencies met: ENABLE_PROCESSING=True")
    print("[PASS] Required option provided: OUTPUT_FILE=output.txt")
    print("[PASS] Validation passed")
    print()


def test_dependency_validation_failure():
    """Test 7: Dependency validation fails when requirements not met."""
    print("=" * 60)
    print("Test 7: Dependency Validation (Failure)")
    print("=" * 60)
    
    parser = argparse.ArgumentParser()
    writer = ArgumentWriter(schema=OPTIONS_SCHEMA_WITH_DEPS)
    writer.add_arguments(parser)
    
    # Enable processing but DON'T provide required output file
    args = parser.parse_args(['--enable-processing'])
    
    log_file = Path('tests/core/options/logs/test_dep_fail.log')
    
    try:
        options = Options(args=args, schema=OPTIONS_SCHEMA_WITH_DEPS, log_file=log_file)
        print("[FAIL] Should have raised ValueError")
        assert False, "Expected ValueError for missing dependency"
    except ValueError as e:
        assert "OUTPUT_FILE is required" in str(e)
        assert "ENABLE_PROCESSING" in str(e)
        print("[PASS] ValueError raised correctly")
        print(f"[PASS] Error message: {str(e)}")
        print()


def test_root_option_auto_default():
    """Test 8: Root options auto-default to True when not explicitly set."""
    print("=" * 60)
    print("Test 8: Root Option Auto-Default")
    print("=" * 60)
    
    # Don't set enable_processing at all (uses schema with dependencies)
    log_file = Path('tests/core/options/logs/test_auto_default.log')
    
    # When root option is auto-defaulted to True, dependent option is required
    # This should fail validation
    try:
        options = Options(schema=OPTIONS_SCHEMA_WITH_DEPS, log_file=log_file)
        print("[FAIL] Should have raised ValueError for missing dependent option")
        assert False
    except ValueError as e:
        assert "OUTPUT_FILE is required" in str(e)
        print("[PASS] Root option auto-defaulted to True")
        print("[PASS] Validation correctly requires dependent option")
        print()


def test_root_option_explicit_false():
    """Test 9: Root options can be explicitly set to False."""
    print("=" * 60)
    print("Test 9: Explicit False for Root Option")
    print("=" * 60)
    
    # Explicitly set to False via environment
    os.environ['ENABLE_PROCESSING'] = 'false'
    
    try:
        log_file = Path('tests/core/options/logs/test_explicit_false.log')
        options = Options(schema=OPTIONS_SCHEMA_WITH_DEPS, log_file=log_file)
        
        # Should respect explicit False and not require dependent option
        assert options.enable_processing is False
        assert options.output_file is None  # Not required when processing disabled
        
        print("[PASS] Env var explicitly set to: false")
        print("[PASS] Root option value: False")
        print("[PASS] No auto-default when explicitly set")
        print("[PASS] Dependent option not required")
        print()
        
    finally:
        del os.environ['ENABLE_PROCESSING']


def test_sensitive_data_masking():
    """Test 10: Sensitive data is masked in logs."""
    print("=" * 60)
    print("Test 10: Sensitive Data Masking")
    print("=" * 60)
    
    os.environ['API_KEY'] = 'secret123'
    
    try:
        log_file = Path('tests/core/options/logs/test_sensitive.log')
        options = Options(schema=OPTIONS_SCHEMA_BASIC, log_file=log_file)
        
        # API key should be set
        assert options.api_key == 'secret123'
        
        # Check log file doesn't contain the actual key
        with open(log_file, 'r') as f:
            log_content = f.read()
            assert 'secret123' not in log_content
            assert '***HIDDEN***' in log_content
        
        print("[PASS] API key set: secret123")
        print("[PASS] Log file masks sensitive data: ***HIDDEN***")
        print()
        
    finally:
        del os.environ['API_KEY']


def test_type_conversions():
    """Test 11: Type conversions from environment variables."""
    print("=" * 60)
    print("Test 11: Type Conversions")
    print("=" * 60)
    
    os.environ['MAX_RETRIES'] = '42'
    os.environ['DATA_DIR'] = '/custom/path'
    os.environ['LOG_LEVEL'] = 'ERROR'
    
    try:
        log_file = Path('tests/core/options/logs/test_types.log')
        options = Options(schema=OPTIONS_SCHEMA_BASIC, log_file=log_file)
        
        # Verify types
        assert isinstance(options.max_retries, int)
        assert options.max_retries == 42
        
        assert isinstance(options.data_dir, Path)
        assert options.data_dir == Path('/custom/path')
        
        assert isinstance(options.log_level, str)
        assert options.log_level == 'ERROR'
        
        print("[PASS] String '42' converted to int: 42")
        print("[PASS] String '/custom/path' converted to Path")
        print("[PASS] Literal choice 'ERROR' validated: ERROR")
        print()
        
    finally:
        del os.environ['MAX_RETRIES']
        del os.environ['DATA_DIR']
        del os.environ['LOG_LEVEL']


def test_literal_type_validation():
    """Test 12: Literal types validate choices from environment."""
    print("=" * 60)
    print("Test 12: Literal Type Validation")
    print("=" * 60)
    
    # Valid choice
    os.environ['LOG_LEVEL'] = 'WARNING'
    
    try:
        log_file = Path('tests/core/options/logs/test_literal.log')
        options = Options(schema=OPTIONS_SCHEMA_BASIC, log_file=log_file)
        
        assert options.log_level == 'WARNING'
        
        print("[PASS] Valid Literal choice accepted: WARNING")
        
    finally:
        del os.environ['LOG_LEVEL']
    
    # Invalid choice should fall back to default
    os.environ['LOG_LEVEL'] = 'INVALID'
    
    try:
        log_file = Path('tests/core/options/logs/test_literal_invalid.log')
        options = Options(schema=OPTIONS_SCHEMA_BASIC, log_file=log_file)
        
        # Should fall back to default
        assert options.log_level == 'INFO'
        
        print("[PASS] Invalid choice 'INVALID' falls back to default: INFO")
        print()
        
    finally:
        del os.environ['LOG_LEVEL']


def test_init_options_helper():
    """Test 13: init_options() helper function."""
    print("=" * 60)
    print("Test 13: init_options() Helper")
    print("=" * 60)
    
    from optionsconfig import init_options
    
    log_file = Path('tests/core/options/logs/test_init_helper.log')
    options = init_options(schema=OPTIONS_SCHEMA_BASIC, log_file=log_file)
    
    assert isinstance(options, Options)
    assert hasattr(options, 'project_name')
    assert options.project_name == "MyProject"
    
    print("[PASS] init_options() returns Options instance")
    print("[PASS] Options correctly initialized")
    print()


def test_schema_attributes():
    """Test 14: All schema options become attributes."""
    print("=" * 60)
    print("Test 14: Schema to Attributes Mapping")
    print("=" * 60)
    
    log_file = Path('tests/core/options/logs/test_attributes.log')
    options = Options(schema=OPTIONS_SCHEMA_BASIC, log_file=log_file)
    
    # Check all schema keys become lowercase attributes
    assert hasattr(options, 'project_name')       # PROJECT_NAME
    assert hasattr(options, 'data_dir')           # DATA_DIR
    assert hasattr(options, 'log_level')          # LOG_LEVEL
    assert hasattr(options, 'api_key')            # API_KEY
    assert hasattr(options, 'max_retries')        # MAX_RETRIES
    
    # Check schema is stored
    assert hasattr(options, 'schema')
    assert len(options.schema) == 5
    
    print("[PASS] All 5 schema options mapped to attributes")
    print("[PASS] UPPER_CASE keys converted to lower_case attributes")
    print("[PASS] Schema stored in options.schema")
    print()


def main():
    """Run all tests."""
    try:
        test_basic_initialization()
        test_log_file_parameter()
        test_args_priority()
        test_env_variables()
        test_args_override_env()
        test_dependency_validation_success()
        test_dependency_validation_failure()
        test_root_option_auto_default()
        test_root_option_explicit_false()
        test_sensitive_data_masking()
        test_type_conversions()
        test_literal_type_validation()
        test_init_options_helper()
        test_schema_attributes()
        
        print("=" * 60)
        print("All Options tests passed!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n[FAIL] Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"\n[FAIL] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
