"""
Tests for examples/direct-pass/ directory
Verifies that running the example produces expected output files
"""

import unittest
import subprocess
import sys
from pathlib import Path
import shutil
import os
import re


class TestDirectPassExample(unittest.TestCase):
    """Test the direct-pass example directory"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment once for all tests"""
        cls.example_dir = Path(__file__).parent.parent.parent / "examples" / "direct-pass"
        cls.test_dir = Path(__file__).parent / "temp_direct_pass"
        
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
        
        # Reset README.md to original state
        readme_path = self.test_dir / "README.md"
        if readme_path.exists():
            readme_path.unlink()
        # Create minimal README for testing
        with open(readme_path, 'w') as f:
            f.write("# Sample Readme\n\n")
            f.write("<!-- BEGIN_GENERATED_OPTIONS -->\n")
            f.write("<!-- END_GENERATED_OPTIONS -->\n")
    
    def test_build_docs_generates_env_example(self):
        """Test that build_docs.py generates .env.example correctly"""
        # Skip if no expected file
        if ".env.example" not in self.expected_files:
            self.skipTest("No expected_.env.example file found")
        
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
        
        # Read generated content
        with open(env_example_path, 'r') as f:
            generated = f.read()
        
        # Read expected content
        expected_path = self.expected_files[".env.example"]
        with open(expected_path, 'r') as f:
            expected = f.read()
        
        self.assertEqual(generated, expected, ".env.example content doesn't match expected")
    
    def test_build_docs_generates_readme(self):
        """Test that build_docs.py generates README.md correctly"""
        # Skip if no expected file
        if "README.md" not in self.expected_files:
            self.skipTest("No expected_README.md file found")
        
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
        
        # Read generated content
        with open(readme_path, 'r') as f:
            generated = f.read()
        
        # Read expected content
        expected_path = self.expected_files["README.md"]
        with open(expected_path, 'r') as f:
            expected = f.read()
        
        # Normalize line endings and trailing whitespace for comparison
        generated_normalized = generated.rstrip()
        expected_normalized = expected.rstrip()
        
        self.assertEqual(generated_normalized, expected_normalized, "README.md content doesn't match expected")
    
    def test_run_with_enable_feature_generates_log(self):
        """Test that run.py --enable-feature generates expected log output"""
        # Skip if no expected file
        if "default.log" not in self.expected_files:
            self.skipTest("No expected_default.log file found")
        
        # Run with --enable-feature
        result = subprocess.run(
            [sys.executable, "run.py", "--enable-feature"],
            cwd=self.test_dir,
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 0, f"run.py failed: {result.stderr}")
        
        # Check log file was created
        log_path = self.test_dir / "default.log"
        self.assertTrue(log_path.exists(), "default.log not generated")
        
        # Read generated log
        with open(log_path, 'r') as f:
            generated_lines = f.readlines()
        
        # Read expected log
        expected_path = self.expected_files["default.log"]
        with open(expected_path, 'r') as f:
            expected_lines = f.readlines()
        
        # Compare line by line, ignoring timestamps and file paths
        self.assertEqual(len(generated_lines), len(expected_lines), 
                        f"Log line count mismatch. Expected {len(expected_lines)}, got {len(generated_lines)}")
        
        for i, (gen_line, exp_line) in enumerate(zip(generated_lines, expected_lines)):
            # Extract message part (after the timestamp and level)
            gen_parts = gen_line.split(' | ', 2)
            exp_parts = exp_line.split(' | ', 2)
            
            if len(gen_parts) >= 3 and len(exp_parts) >= 3:
                # Compare level and message
                gen_level = gen_parts[0].strip()
                exp_level = exp_parts[0].strip()
                gen_msg = gen_parts[2].strip()
                exp_msg = exp_parts[2].strip()
                
                self.assertEqual(gen_level, exp_level, 
                               f"Line {i+1}: Log level mismatch")
                
                # For path-containing messages, normalize paths
                if "Loaded .env from:" in gen_msg or "Logging initialized to:" in gen_msg:
                    # Just check the message type matches
                    self.assertTrue(gen_msg.startswith(exp_msg.split(':')[0]), 
                                  f"Line {i+1}: Message type mismatch")
                else:
                    self.assertEqual(gen_msg, exp_msg, 
                                   f"Line {i+1}: Message mismatch")
    
    def test_run_help_displays_arguments(self):
        """Test that run.py --help displays the schema arguments"""
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


if __name__ == "__main__":
    unittest.main()
