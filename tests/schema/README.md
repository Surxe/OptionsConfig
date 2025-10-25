# Schema Module Tests

This directory contains tests for `src/optionsconfig/schema.py`.

## Overview

The schema module is responsible for loading and validating `OPTIONS_SCHEMA` dictionaries from various sources:
1. Direct parameter passed to `get_schema()`
2. Configuration file (`pyproject.toml`)

## Test Files

- **`test_schema.py`** - Main test suite (5 tests)
- **`sample_schema.py`** - Sample OPTIONS_SCHEMA for testing

## Running Tests

```bash
python tests/schema/test_schema.py
```

## Test Coverage

### Test 1: Direct Schema Parameter
- **Purpose**: Verify `get_schema(schema=dict)` accepts and returns direct schema
- **Coverage**: Direct parameter priority (highest)

### Test 2: No Schema Parameter, No Config
- **Purpose**: Verify `get_schema()` raises ImportError when no schema available
- **Coverage**: Error handling when no schema source exists

### Test 3: Load from Config - No File
- **Purpose**: Verify `_load_schema_from_config()` returns None when pyproject.toml missing
- **Coverage**: Graceful handling of missing config file

### Test 4: OptionDefinition TypedDict
- **Purpose**: Verify the OptionDefinition TypedDict structure
- **Coverage**: TypedDict with total=False (all fields optional)
- **Fields Tested**:
  - `env`: str
  - `arg`: str
  - `type`: Any
  - `default`: Any
  - `section`: str
  - `help`: str
  - `depends_on`: Optional[List[str]]
  - `sensitive`: Optional[bool]

### Test 5: Load Existing Sample Schema
- **Purpose**: Verify sample_schema.py can be loaded and used
- **Coverage**: Real-world schema loading from module

## Schema Module Functions

### `get_schema(schema=None) -> dict`
Load OPTIONS_SCHEMA from available sources with priority:
1. Direct schema parameter (if provided)
2. Configuration file (pyproject.toml)

Raises `ImportError` if no schema found.

### `_load_schema_from_config() -> dict | None`
Internal function to load schema module path from `pyproject.toml`.

Returns `None` if:
- pyproject.toml doesn't exist
- [tool.optionsconfig] section missing
- schema_module not configured
- Module import fails

### `OptionDefinition` (TypedDict)
Type definition for individual option entries in OPTIONS_SCHEMA.

## Test Isolation

Tests use `tempfile.mkdtemp()` with proper cleanup:
```python
tmpdir = None
try:
    tmpdir = tempfile.mkdtemp()
    # ... test code ...
finally:
    if tmpdir:
        shutil.rmtree(tmpdir, ignore_errors=True)
```

This ensures:
- Each test gets clean temporary directory
- No leftover files after test run
- Windows file lock issues handled with `ignore_errors=True`

## Expected Output

```
============================================================
Test 1: Direct Schema Parameter
============================================================
[PASS] Direct schema parameter accepted
[PASS] Schema returned unchanged

============================================================
Test 2: No Schema Parameter, No Config
============================================================
[PASS] ImportError raised correctly

============================================================
Test 3: Load from Config - No File
============================================================
[PASS] Returns None when pyproject.toml not found

============================================================
Test 4: OptionDefinition TypedDict
============================================================
[PASS] OptionDefinition TypedDict structure valid
[PASS] All fields accessible

============================================================
Test 5: Load Existing Sample Schema
============================================================
[PASS] sample_schema.py loaded successfully
[PASS] Contains SHOULD_PARSE and GAME_NAME
[PASS] Works with get_schema()

============================================================
All 5 schema tests passed!
============================================================
```

## Notes

- Tests use `sys.path.insert(0, ...)` to import from local src directory
- Schema loading priority: direct param > config file
- All test functions can be run independently
- No external dependencies required (uses sample_schema.py for schema tests)
