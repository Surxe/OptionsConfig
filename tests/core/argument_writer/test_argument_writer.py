#!/usr/bin/env python3
"""
Test suite for ArgumentWriter class

Tests argument generation for various types:
- Boolean arguments (store_true)
- String arguments
- Integer arguments
- Float arguments
- Path arguments
- Literal (choice) arguments
"""

import sys
from pathlib import Path
import argparse

# Add src to path for local testing
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

from optionsconfig import ArgumentWriter

# Import the test schema from this directory
from options_schema import OPTIONS_SCHEMA


def test_initialization():
    """Test ArgumentWriter initialization with schema."""
    print("=" * 60)
    print("Test 1: ArgumentWriter Initialization")
    print("=" * 60)
    
    writer = ArgumentWriter(schema=OPTIONS_SCHEMA)
    assert writer.schema is not None
    assert len(writer.schema) == 7  # We have 7 options in test schema
    
    print("[PASS] ArgumentWriter initialized successfully")
    print(f"[PASS] Schema contains {len(writer.schema)} options")
    print()


def test_boolean_argument():
    """Test that boolean arguments are created with store_true action."""
    print("=" * 60)
    print("Test 2: Boolean Argument (--verbose)")
    print("=" * 60)
    
    parser = argparse.ArgumentParser()
    writer = ArgumentWriter(schema=OPTIONS_SCHEMA)
    writer.add_arguments(parser)
    
    # Test without flag
    args = parser.parse_args([])
    assert args.verbose is None, f"Expected None, got {args.verbose}"
    print("[PASS] Without flag: verbose=None")
    
    # Test with flag
    args = parser.parse_args(['--verbose'])
    assert args.verbose is True, f"Expected True, got {args.verbose}"
    print("[PASS] With flag: verbose=True")
    print()


def test_string_argument():
    """Test string argument creation."""
    print("=" * 60)
    print("Test 3: String Argument (--output-file)")
    print("=" * 60)
    
    parser = argparse.ArgumentParser()
    writer = ArgumentWriter(schema=OPTIONS_SCHEMA)
    writer.add_arguments(parser)
    
    # Test default (None since we use default=None in add_argument)
    args = parser.parse_args([])
    assert args.output_file is None, f"Expected None, got {args.output_file}"
    print("[PASS] Without arg: output_file=None")
    
    # Test with value
    args = parser.parse_args(['--output-file', 'test.txt'])
    assert args.output_file == 'test.txt', f"Expected 'test.txt', got {args.output_file}"
    print("[PASS] With arg: output_file='test.txt'")
    print()


def test_integer_argument():
    """Test integer argument creation."""
    print("=" * 60)
    print("Test 4: Integer Argument (--max-workers)")
    print("=" * 60)
    
    parser = argparse.ArgumentParser()
    writer = ArgumentWriter(schema=OPTIONS_SCHEMA)
    writer.add_arguments(parser)
    
    # Test default
    args = parser.parse_args([])
    assert args.max_workers is None
    print("[PASS] Without arg: max_workers=None")
    
    # Test with value
    args = parser.parse_args(['--max-workers', '8'])
    assert args.max_workers == 8, f"Expected 8, got {args.max_workers}"
    assert isinstance(args.max_workers, int), f"Expected int, got {type(args.max_workers)}"
    print("[PASS] With arg: max_workers=8 (int)")
    print()


def test_float_argument():
    """Test float argument creation."""
    print("=" * 60)
    print("Test 5: Float Argument (--threshold)")
    print("=" * 60)
    
    parser = argparse.ArgumentParser()
    writer = ArgumentWriter(schema=OPTIONS_SCHEMA)
    writer.add_arguments(parser)
    
    # Test default
    args = parser.parse_args([])
    assert args.threshold is None
    print("[PASS] Without arg: threshold=None")
    
    # Test with value
    args = parser.parse_args(['--threshold', '0.75'])
    assert args.threshold == 0.75, f"Expected 0.75, got {args.threshold}"
    assert isinstance(args.threshold, float), f"Expected float, got {type(args.threshold)}"
    print("[PASS] With arg: threshold=0.75 (float)")
    print()


def test_path_argument():
    """Test Path argument creation (handled as string)."""
    print("=" * 60)
    print("Test 6: Path Argument (--data-dir)")
    print("=" * 60)
    
    parser = argparse.ArgumentParser()
    writer = ArgumentWriter(schema=OPTIONS_SCHEMA)
    writer.add_arguments(parser)
    
    # Test default
    args = parser.parse_args([])
    assert args.data_dir is None
    print("[PASS] Without arg: data_dir=None")
    
    # Test with value
    args = parser.parse_args(['--data-dir', '/path/to/data'])
    assert args.data_dir == '/path/to/data', f"Expected '/path/to/data', got {args.data_dir}"
    # ArgumentWriter converts Path to str type for argparse
    assert isinstance(args.data_dir, str), f"Expected str, got {type(args.data_dir)}"
    print("[PASS] With arg: data_dir='/path/to/data' (str)")
    print()


def test_literal_argument():
    """Test Literal (choice) argument creation."""
    print("=" * 60)
    print("Test 7: Literal Argument (--log-level)")
    print("=" * 60)
    
    parser = argparse.ArgumentParser()
    writer = ArgumentWriter(schema=OPTIONS_SCHEMA)
    writer.add_arguments(parser)
    
    # Test default
    args = parser.parse_args([])
    assert args.log_level is None
    print("[PASS] Without arg: log_level=None")
    
    # Test with valid choice
    args = parser.parse_args(['--log-level', 'DEBUG'])
    assert args.log_level == 'DEBUG', f"Expected 'DEBUG', got {args.log_level}"
    print("[PASS] With valid choice: log_level='DEBUG'")
    
    # Test invalid choice should raise error
    try:
        args = parser.parse_args(['--log-level', 'INVALID'])
        print("[FAIL] Invalid choice should have raised error")
        assert False, "Should have raised SystemExit"
    except SystemExit:
        print("[PASS] Invalid choice 'INVALID' rejected correctly")
    print()


def test_all_arguments_together():
    """Test parsing multiple arguments together."""
    print("=" * 60)
    print("Test 8: Multiple Arguments Together")
    print("=" * 60)
    
    parser = argparse.ArgumentParser()
    writer = ArgumentWriter(schema=OPTIONS_SCHEMA)
    writer.add_arguments(parser)
    
    # Parse multiple arguments
    args = parser.parse_args([
        '--verbose',
        '--output-file', 'results.txt',
        '--max-workers', '12',
        '--threshold', '0.8',
        '--data-dir', '/data',
        '--log-level', 'WARNING'
    ])
    
    assert args.verbose is True
    assert args.output_file == 'results.txt'
    assert args.max_workers == 12
    assert args.threshold == 0.8
    assert args.data_dir == '/data'
    assert args.log_level == 'WARNING'
    
    print("[PASS] All arguments parsed correctly:")
    print(f"  verbose: {args.verbose}")
    print(f"  output_file: {args.output_file}")
    print(f"  max_workers: {args.max_workers}")
    print(f"  threshold: {args.threshold}")
    print(f"  data_dir: {args.data_dir}")
    print(f"  log_level: {args.log_level}")
    print()


def test_help_text():
    """Test that help text is generated correctly."""
    print("=" * 60)
    print("Test 9: Help Text Generation")
    print("=" * 60)
    
    parser = argparse.ArgumentParser()
    writer = ArgumentWriter(schema=OPTIONS_SCHEMA)
    writer.add_arguments(parser)
    
    # Get the actions from the parser
    actions = {action.dest: action for action in parser._actions if action.dest != 'help'}
    
    # Check that help text includes default values
    verbose_action = actions['verbose']
    assert '(default: False)' in verbose_action.help
    print("[PASS] Help text for --verbose includes default: False")
    
    output_file_action = actions['output_file']
    assert '(default: output.txt)' in output_file_action.help
    print("[PASS] Help text for --output-file includes default: output.txt")
    
    max_workers_action = actions['max_workers']
    assert '(default: 4)' in max_workers_action.help
    print("[PASS] Help text for --max-workers includes default: 4")
    print()


def test_reinitialization():
    """Test creating multiple ArgumentWriter instances."""
    print("=" * 60)
    print("Test 10: Multiple ArgumentWriter Instances")
    print("=" * 60)
    
    # Create first instance
    writer1 = ArgumentWriter(schema=OPTIONS_SCHEMA)
    parser1 = argparse.ArgumentParser()
    writer1.add_arguments(parser1)
    
    # Create second instance
    writer2 = ArgumentWriter(schema=OPTIONS_SCHEMA)
    parser2 = argparse.ArgumentParser()
    writer2.add_arguments(parser2)
    
    # Both should work independently
    args1 = parser1.parse_args(['--verbose'])
    args2 = parser2.parse_args(['--max-workers', '16'])
    
    assert args1.verbose is True
    assert args2.max_workers == 16
    
    print("[PASS] Multiple ArgumentWriter instances work independently")
    print()


def main():
    """Run all tests."""
    try:
        test_initialization()
        test_boolean_argument()
        test_string_argument()
        test_integer_argument()
        test_float_argument()
        test_path_argument()
        test_literal_argument()
        test_all_arguments_together()
        test_help_text()
        test_reinitialization()
        
        print("=" * 60)
        print("All ArgumentWriter tests passed!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n[FAIL] Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[FAIL] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
