# Options Class Tests

Comprehensive test suite for the `Options` class covering initialization, configuration, validation, and all features.

## Test Structure

```
tests/core/options/
├── options_schema.py       # Test schemas (basic and with dependencies)
├── test_options.py         # Comprehensive test suite (14 tests)
└── README.md              # This file
```

## Test Coverage

### **Core Functionality Tests**

#### 1. **Basic Initialization**
- Schema loading and attribute creation
- Default value assignment
- Lowercase attribute naming (UPPER_CASE → lower_case)

#### 2. **Log File Parameter**
- Custom log file path specification
- Automatic directory creation
- File creation validation

#### 3. **Argument Priority**
- Command-line arguments override defaults
- Non-specified args retain defaults
- ArgumentWriter integration

### **Priority System Tests**

#### 4. **Environment Variable Priority**
- Environment variables override defaults
- Type conversions from strings
- Proper value assignment

#### 5. **Args Override Env Variables**
- Full priority chain: args > env > defaults
- Correct precedence handling

### **Dependency Validation Tests**

#### 6. **Dependency Validation (Success)**
- Required dependencies properly validated
- Options with depends_on work correctly
- Validation passes when requirements met

#### 7. **Dependency Validation (Failure)**
- ValueError raised for missing dependencies
- Clear error messages
- Lists active dependencies

### **Root Option Tests**

#### 8. **Root Option Auto-Default**
- Root options auto-default to True
- Only when not explicitly set
- Triggers dependency validation

#### 9. **Explicit False for Root Option**
- Can explicitly set root options to False
- No auto-default when explicitly set
- Dependent options not required when False

### **Security & Type Tests**

#### 10. **Sensitive Data Masking**
- Sensitive fields marked in schema
- Values masked in logs (***HIDDEN***)
- Actual values accessible in code

#### 11. **Type Conversions**
- String to int conversion
- String to Path conversion
- Literal type validation

#### 12. **Literal Type Validation**
- Valid choices accepted
- Invalid choices fall back to default
- Type safety enforced

### **Helper & API Tests**

#### 13. **init_options() Helper**
- Helper function works correctly
- Returns Options instance
- Accepts all parameters

#### 14. **Schema to Attributes Mapping**
- All schema keys become attributes
- Naming conversion works (UPPER → lower)
- Schema stored in options.schema

## Test Schemas

### OPTIONS_SCHEMA_BASIC
Basic schema without dependencies (5 options):
- `PROJECT_NAME` - String with default
- `DATA_DIR` - Path with default  
- `LOG_LEVEL` - Literal choices
- `API_KEY` - Sensitive string
- `MAX_RETRIES` - Integer

### OPTIONS_SCHEMA_WITH_DEPS
Schema with dependency relationships (3 options):
- `ENABLE_PROCESSING` - Root boolean option
- `OUTPUT_FILE` - Path depending on ENABLE_PROCESSING
- `PROJECT_NAME` - Independent string option

## Running Tests

```bash
# Run from repository root
python tests/core/options/test_options.py
```

## Expected Output

All 14 tests should pass with output showing:
- Test number and description
- [PASS] indicators for each assertion
- Final success message

## Test Design Principles

1. **Comprehensive Coverage** - All Options features tested
2. **Isolation** - Each test is independent
3. **Multiple Schemas** - Separate schemas for basic vs dependency tests
4. **Environment Safety** - Env vars properly cleaned up
5. **Clear Output** - Progress messages for each test
6. **Type Verification** - Both values and types checked
7. **Error Testing** - Both success and failure paths tested

## Key Features Tested

✅ Direct schema parameter support  
✅ Log file configuration (direct, config, default)  
✅ Priority system (args > env > defaults)  
✅ Root option auto-defaulting  
✅ Dependency validation with clear errors  
✅ Type conversions (int, Path, bool, Literal)  
✅ Sensitive data masking  
✅ Environment variable handling  
✅ Helper functions (init_options)  
✅ Schema to attribute mapping  
