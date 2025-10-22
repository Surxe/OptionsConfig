#!/usr/bin/env python3
"""Basic test suite for schema.py module."""

import sys
import os
from pathlib import Path
import tempfile
import shutil

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from optionsconfig.schema import get_schema, _load_schema_from_config, OptionDefinition


def test_get_schema_with_direct_param():
    """Test 1: get_schema() with direct schema parameter."""
    print("=" * 60)
    print("Test 1: Direct Schema Parameter")
    print("=" * 60)
    
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
    
    assert result == test_schema
    assert "TEST_OPTION" in result
    assert result["TEST_OPTION"]["default"] == "test"
    
    print("[PASS] Direct schema parameter accepted")
    print("[PASS] Schema returned unchanged")
    print()


def test_get_schema_without_param_no_config():
    """Test 2: get_schema() without parameter and no config file."""
    print("=" * 60)
    print("Test 2: No Schema Parameter, No Config")
    print("=" * 60)
    
    original_dir = os.getcwd()
    tmpdir = None
    
    try:
        tmpdir = tempfile.mkdtemp()
        os.chdir(tmpdir)
        
        # Should raise ImportError
        try:
            get_schema()
            print("[FAIL] Should have raised ImportError")
            assert False
        except ImportError as e:
            assert "No OPTIONS_SCHEMA found" in str(e)
            print("[PASS] ImportError raised correctly")
            print()
    finally:
        os.chdir(original_dir)
        if tmpdir:
            shutil.rmtree(tmpdir, ignore_errors=True)


def test_load_schema_from_config_no_file():
    """Test 3: _load_schema_from_config() with no pyproject.toml."""
    print("=" * 60)
    print("Test 3: Load from Config - No File")
    print("=" * 60)
    
    original_dir = os.getcwd()
    tmpdir = None
    
    try:
        tmpdir = tempfile.mkdtemp()
        os.chdir(tmpdir)
        
        result = _load_schema_from_config()
        
        assert result is None
        print("[PASS] Returns None when pyproject.toml not found")
        print()
    finally:
        os.chdir(original_dir)
        if tmpdir:
            shutil.rmtree(tmpdir, ignore_errors=True)


def test_option_definition_typed_dict():
    """Test 4: OptionDefinition TypedDict structure."""
    print("=" * 60)
    print("Test 4: OptionDefinition TypedDict")
    print("=" * 60)
    
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
    assert option["env"] == "TEST_VAR"
    assert option["arg"] == "--test-var"
    assert option["type"] == str
    assert option["default"] == "value"
    assert option["section"] == "Test"
    assert option["help"] == "Test help text"
    assert option["depends_on"] == ["OTHER_OPTION"]
    assert option["sensitive"] is False
    
    print("[PASS] OptionDefinition TypedDict structure valid")
    print("[PASS] All fields accessible")
    print()


def test_existing_sample_schema():
    """Test 5: Load existing sample_schema.py from tests/schema/."""
    print("=" * 60)
    print("Test 5: Load Existing Sample Schema")
    print("=" * 60)
    
    schema_dir = Path(__file__).parent
    sys.path.insert(0, str(schema_dir))
    
    try:
        from sample_schema import OPTIONS_SCHEMA
        
        assert OPTIONS_SCHEMA is not None
        assert isinstance(OPTIONS_SCHEMA, dict)
        assert "SHOULD_PARSE" in OPTIONS_SCHEMA
        assert "GAME_NAME" in OPTIONS_SCHEMA
        
        # Test get_schema with it
        result = get_schema(schema=OPTIONS_SCHEMA)
        assert result == OPTIONS_SCHEMA
        
        print("[PASS] sample_schema.py loaded successfully")
        print("[PASS] Contains SHOULD_PARSE and GAME_NAME")
        print("[PASS] Works with get_schema()")
        print()
    finally:
        sys.path.remove(str(schema_dir))


def main():
    """Run all tests."""
    try:
        test_get_schema_with_direct_param()
        test_get_schema_without_param_no_config()
        test_load_schema_from_config_no_file()
        test_option_definition_typed_dict()
        test_existing_sample_schema()
        
        print("=" * 60)
        print("All 5 schema tests passed!")
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
