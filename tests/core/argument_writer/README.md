# ArgumentWriter Tests

Comprehensive test suite for the `ArgumentWriter` class.

## Test Structure

```
tests/core/argument_writer/
├── options_schema.py           # Test schema with various option types
└── test_argument_writer.py     # Main test suite
```

## Test Coverage

### 1. **Initialization Test**
- Verifies ArgumentWriter can be initialized with a schema
- Checks that schema is properly stored

### 2. **Boolean Arguments**
- Tests `store_true` action for boolean flags
- Verifies default None and flag=True behavior

### 3. **String Arguments**
- Tests string argument parsing
- Verifies type conversion

### 4. **Integer Arguments**
- Tests integer argument parsing
- Verifies type conversion to int

### 5. **Float Arguments**
- Tests float argument parsing
- Verifies type conversion to float

### 6. **Path Arguments**
- Tests Path argument handling
- Verifies conversion to string for argparse compatibility

### 7. **Literal (Choice) Arguments**
- Tests Literal type with predefined choices
- Verifies valid choices are accepted
- Verifies invalid choices are rejected

### 8. **Multiple Arguments**
- Tests parsing multiple arguments simultaneously
- Verifies all arguments work together correctly

### 9. **Help Text Generation**
- Verifies help text includes default values
- Tests that help messages are formatted correctly

### 10. **Multiple Instances**
- Tests creating multiple ArgumentWriter instances
- Verifies instances work independently

## Test Schema

The test schema includes 7 different option types:

- `VERBOSE` - Boolean (--verbose)
- `OUTPUT_FILE` - String (--output-file)
- `MAX_WORKERS` - Integer (--max-workers)
- `THRESHOLD` - Float (--threshold)
- `DATA_DIR` - Path (--data-dir)
- `LOG_LEVEL` - Literal choice (--log-level)
- `CONFIG_FILE` - Path with dependency (--config-file)

## Running Tests

```bash
# Run from repository root
python tests/core/argument_writer/test_argument_writer.py
```

## Expected Output

All 10 tests should pass with output showing:
- Test name and description
- Verification checkmarks for each assertion
- Final success message

## Test Design Principles

1. **Comprehensive Coverage** - Tests all supported argument types
2. **Clear Output** - Each test prints its progress and results
3. **Isolated Tests** - Each test is independent and can run alone
4. **Type Verification** - Tests verify both values and types
5. **Edge Cases** - Tests invalid inputs and error handling
