#!/usr/bin/env python3
"""Test script for Options class with log_file parameter"""

import sys
from pathlib import Path

# Add src to path for local testing
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from optionsconfig.core import Options

# Import the test schema from this directory
from options_schema import OPTIONS_SCHEMA

def test_options_with_log_file():
    """Test that Options respects the log_file parameter."""
    
    # Setup log file path
    log_file = Path('tests/core/logs/test_options.log')
    
    # Create Options with explicit log_file
    options = Options(schema=OPTIONS_SCHEMA, log_file=log_file)
    
    # Verify log_file was set correctly
    assert options.log_file == log_file, f"Expected log_file to be {log_file}, got {options.log_file}"
    
    # Verify log file was created
    assert log_file.exists(), f"Log file {log_file} was not created"
    
    # Verify parent directory was created
    assert log_file.parent.exists(), f"Log directory {log_file.parent} was not created"
    
    print(f"✓ Log file set to: {options.log_file}")
    print(f"✓ Log file created successfully")
    print(f"✓ Options initialized successfully")

if __name__ == "__main__":
    test_options_with_log_file()
    print("All tests completed!")
