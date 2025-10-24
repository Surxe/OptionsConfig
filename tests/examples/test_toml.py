"""
Tests for examples/toml/ directory
Verifies that running the example with pyproject.toml configuration produces expected output
"""

import unittest
import subprocess
import sys
from pathlib import Path
import shutil
import os
import re


class TestTomlExample(unittest.TestCase):
    """Test the toml example directory"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment once for all tests"""
        cls.example_dir = Path(__file__).parent.parent.parent / "examples" / "toml"
        cls.test_dir = Path(__file__).parent / "temp_toml"
        
        # Create test directory
        cls.test_dir.mkdir(parents=True, exist_ok=True)
        
        # Find all expected files
        cls.expected_files = {}
        for expected_file in cls.example_dir.glob("expected_*"):
            if expected_file.is_file():
                # Map expected_filename -> actual_filename
                actual_name = expected_file.name.replace("expected_", "", 1)
                cls.expected_files[actual_name] = expected_file
        
        # Copy example files to test directory (excluding expected_ files)
        for item in cls.example_dir.iterdir():
            if item.name.startswith("expected_") or item.name == "__pycache__":
                continue
            if item.is_file():
                shutil.copy2(item, cls.test_dir / item.name)
            elif item.is_dir() and item.name != "__pycache__":
                shutil.copytree(item, cls.test_dir / item.name, dirs_exist_ok=True)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test directory after all tests"""
        if cls.test_dir.exists():
            shutil.rmtree(cls.test_dir)
    
    def setUp(self):
        """Clean up generated files before each test"""
        # Remove generated files
        for file in [".env.example", "default.log"]:
            file_path = self.test_dir / file
            if file_path.exists():
                file_path.unlink()
        
        # Reset README.md if it exists
        readme_path = self.test_dir / "README.md"
        if readme_path.exists():
            readme_path.unlink()
        # Create minimal README for testing
        with open(readme_path, 'w') as f:
            f.write("# Sample Readme\n\n")
            f.write("<!-- BEGIN_GENERATED_OPTIONS -->\n")
            f.write("<!-- END_GENERATED_OPTIONS -->\n")
    
    def test_pyproject_toml_exists(self):
        """Test that pyproject.toml exists with correct configuration"""
        pyproject_path = self.test_dir / "pyproject.toml"
        self.assertTrue(pyproject_path.exists(), "pyproject.toml not found")
        
        # Read and verify content
        with open(pyproject_path, 'r') as f:
            content = f.read()
        
        self.assertIn("[tool.optionsconfig]", content)
        self.assertIn('schema_module = "options_schema"', content)
        self.assertIn('log_file = "default.log"', content)
    
    def test_build_docs_generates_env_example(self):
        """Test that build_docs.py generates .env.example using pyproject.toml"""
        # Run build_docs.py
        result = subprocess.run(
            [sys.executable, "build_docs.py"],
            cwd=self.test_dir,
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 0, f"build_docs.py failed: {result.stderr}")
        
        # Check .env.example was created
        env_example_path = self.test_dir / ".env.example"
        self.assertTrue(env_example_path.exists(), ".env.example not generated")
        
        # If expected file exists, compare against it
        if ".env.example" in self.expected_files:
            with open(env_example_path, 'r') as f:
                generated = f.read()
            with open(self.expected_files[".env.example"], 'r') as f:
                expected = f.read()
            self.assertEqual(generated, expected, ".env.example content doesn't match expected")
        else:
            # Otherwise, verify content has expected structure
            with open(env_example_path, 'r') as f:
                content = f.read()
            
            self.assertIn("ENABLE_FEATURE", content)
            self.assertIn("FEATURE_PATH", content)
            self.assertIn("Features", content)
            self.assertIn("Enable the special feature", content)
    
    def test_build_docs_generates_readme(self):
        """Test that build_docs.py generates README.md using pyproject.toml"""
        # Run build_docs.py
        result = subprocess.run(
            [sys.executable, "build_docs.py"],
            cwd=self.test_dir,
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 0, f"build_docs.py failed: {result.stderr}")
        
        # Check README.md was updated
        readme_path = self.test_dir / "README.md"
        self.assertTrue(readme_path.exists(), "README.md not found")
        
        # If expected file exists, compare against it
        if "README.md" in self.expected_files:
            with open(readme_path, 'r') as f:
                generated = f.read()
            with open(self.expected_files["README.md"], 'r') as f:
                expected = f.read()
            # Normalize line endings and trailing whitespace
            self.assertEqual(generated.rstrip(), expected.rstrip(), "README.md content doesn't match expected")
        else:
            # Otherwise, verify content has expected structure
            with open(readme_path, 'r') as f:
                content = f.read()
            
            self.assertIn("ENABLE_FEATURE", content)
            self.assertIn("FEATURE_PATH", content)
            self.assertIn("--enable-feature", content)
            self.assertIn("--feature-path", content)
            self.assertIn("Depends on: `ENABLE_FEATURE`", content)
    
    def test_run_with_enable_feature_uses_pyproject_config(self):
        """Test that run.py --enable-feature loads schema from pyproject.toml"""
        # Run with --enable-feature
        result = subprocess.run(
            [sys.executable, "run.py", "--enable-feature"],
            cwd=self.test_dir,
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 0, f"run.py failed: {result.stderr}")
        
        # Check log file was created (as specified in pyproject.toml)
        log_path = self.test_dir / "default.log"
        self.assertTrue(log_path.exists(), "default.log not generated")
        
        # If expected log file exists, compare against it
        if "default.log" in self.expected_files:
            with open(log_path, 'r') as f:
                generated_lines = f.readlines()
            with open(self.expected_files["default.log"], 'r') as f:
                expected_lines = f.readlines()
            
            # Compare line by line, ignoring timestamps and file paths
            self.assertEqual(len(generated_lines), len(expected_lines), 
                           f"Log line count mismatch. Expected {len(expected_lines)}, got {len(generated_lines)}")
            
            for i, (gen_line, exp_line) in enumerate(zip(generated_lines, expected_lines)):
                gen_parts = gen_line.split(' | ', 2)
                exp_parts = exp_line.split(' | ', 2)
                
                if len(gen_parts) >= 3 and len(exp_parts) >= 3:
                    gen_level = gen_parts[0].strip()
                    exp_level = exp_parts[0].strip()
                    gen_msg = gen_parts[2].strip()
                    exp_msg = exp_parts[2].strip()
                    
                    self.assertEqual(gen_level, exp_level, f"Line {i+1}: Log level mismatch")
                    
                    # For path-containing messages, just check message type
                    if "Loaded .env from:" in gen_msg or "Logging initialized to:" in gen_msg:
                        self.assertTrue(gen_msg.startswith(exp_msg.split(':')[0]), 
                                      f"Line {i+1}: Message type mismatch")
                    else:
                        self.assertEqual(gen_msg, exp_msg, f"Line {i+1}: Message mismatch")
        else:
            # Otherwise, verify log contains expected operations
            with open(log_path, 'r') as f:
                log_content = f.read()
            
            self.assertIn("Logging initialized to:", log_content)
            self.assertIn("Added boolean argument --enable-feature", log_content)
            self.assertIn("Added argument --feature-path", log_content)
            self.assertIn("Options initialized with:", log_content)
            self.assertIn("ENABLE_FEATURE: True", log_content)
            self.assertIn("FEATURE_PATH:", log_content)
            self.assertIn("Example Retrieval of enable_feature: True", log_content)
    
    def test_run_help_displays_arguments(self):
        """Test that run.py --help displays the schema arguments loaded from pyproject.toml"""
        result = subprocess.run(
            [sys.executable, "run.py", "--help"],
            cwd=self.test_dir,
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 0, f"run.py --help failed: {result.stderr}")
        
        # Check that help output contains our arguments
        self.assertIn("--enable-feature", result.stdout)
        self.assertIn("--feature-path", result.stdout)
        self.assertIn("Enable the special feature", result.stdout)
        self.assertIn("Path to the feature configuration file", result.stdout)
    
    def test_run_without_args_uses_env_values(self):
        """Test that run.py without args uses values from .env file"""
        # Run without arguments
        result = subprocess.run(
            [sys.executable, "run.py"],
            cwd=self.test_dir,
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 0, f"run.py failed: {result.stderr}")
        
        # Check log shows values loaded from .env
        log_path = self.test_dir / "default.log"
        self.assertTrue(log_path.exists(), "default.log not generated")
        
        with open(log_path, 'r') as f:
            log_content = f.read()
        
        # Should see values loaded from .env file
        self.assertIn("Loaded .env from:", log_content)
        self.assertIn("Environment variable ENABLE_FEATURE found with value: True", log_content)
        self.assertIn("ENABLE_FEATURE: True", log_content)
        self.assertIn("FEATURE_PATH: path/to/something", log_content)
    
    def test_schema_loaded_from_pyproject(self):
        """Test that schema is successfully loaded from pyproject.toml configuration"""
        # Create a simple test script that imports and checks schema
        test_script = self.test_dir / "test_schema_load.py"
        with open(test_script, 'w') as f:
            f.write("""
from optionsconfig.schema import get_schema

schema = get_schema()
assert "ENABLE_FEATURE" in schema
assert "FEATURE_PATH" in schema
print("Schema loaded successfully from pyproject.toml")
""")
        
        result = subprocess.run(
            [sys.executable, "test_schema_load.py"],
            cwd=self.test_dir,
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 0, f"Schema load test failed: {result.stderr}")
        self.assertIn("Schema loaded successfully", result.stdout)
        
        # Clean up test script
        test_script.unlink()


if __name__ == "__main__":
    unittest.main()
