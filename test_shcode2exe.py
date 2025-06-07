#!/usr/bin/env python3

import os
import sys
import subprocess
import tempfile
import shutil

def get_python_command():
    """Detect the available Python command"""
    # Try python3 first, then python
    for cmd in ['python3', 'python']:
        try:
            result = subprocess.run([cmd, '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                # Check if it's Python 3.x
                if 'Python 3' in result.stdout or 'Python 3' in result.stderr:
                    return cmd
        except FileNotFoundError:
            continue
    
    print("❌ ERROR: No Python 3 interpreter found!")
    print("Please ensure Python 3 is installed and in your PATH")
    sys.exit(1)

def setup_path():
    """Add bundled tools to PATH if needed"""
    tools_nasm = os.path.join(os.path.dirname(__file__), 'tools', 'nasm')
    tools_linkers = os.path.join(os.path.dirname(__file__), 'tools', 'linkers')
    
    # Add to PATH
    os.environ['PATH'] = f"{tools_nasm}{os.pathsep}{tools_linkers}{os.pathsep}{os.environ['PATH']}"
    
    # Make tools executable on Linux/Mac
    if sys.platform != 'win32':
        nasm_path = os.path.join(tools_nasm, 'nasm')
        ld_path = os.path.join(tools_linkers, 'ld')
        if os.path.exists(nasm_path):
            os.chmod(nasm_path, 0o755)
        if os.path.exists(ld_path):
            os.chmod(ld_path, 0o755)

def verify_shellcode_in_exe(exe_path, shellcode_path):
    """Verify that the shellcode is properly embedded in the executable"""
    try:
        # Read the original shellcode
        with open(shellcode_path, 'rb') as f:
            original_shellcode = f.read()
        
        # Read the executable
        with open(exe_path, 'rb') as f:
            exe_data = f.read()
        
        # Search for the shellcode in the executable
        if original_shellcode in exe_data:
            shellcode_offset = exe_data.find(original_shellcode)
            return True, f"Shellcode found at offset 0x{shellcode_offset:04X}"
        else:
            return False, "Shellcode not found in executable"
    except Exception as e:
        return False, f"Error during verification: {e}"

def run_test(test_name, command, expected_file, verify_shellcode=None):
    """Run a test and verify shellcode embedding"""
    print(f"\n[TEST] {test_name}")
    
    try:
        # Run the command
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ FAILED: Command error")
            return False
        
        # Check if output file exists
        if not os.path.exists(expected_file):
            print(f"❌ FAILED: Output file not created")
            return False
        
        # Verify shellcode embedding
        if verify_shellcode:
            success, message = verify_shellcode_in_exe(expected_file, verify_shellcode)
            if success:
                print(f"✅ PASSED: {message}")
                return True
            else:
                print(f"❌ FAILED: {message}")
                return False
        else:
            print(f"✅ PASSED")
            return True
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def main():
    print("=== shcode2exe Test Suite ===")
    
    # Detect Python command early
    python_cmd = get_python_command()
    print(f"Using Python command: {python_cmd}")
    
    # Setup environment
    setup_path()
    
    # Create temp directory for test outputs
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(os.path.dirname(__file__))  # Ensure we're in the right directory
        
        tests_passed = 0
        tests_total = 0
        
        # Detect the available Python command
        python_cmd = get_python_command()
        
        # Test 1: Basic binary shellcode (32-bit)
        tests_total += 1
        output_file = os.path.join(tmpdir, "test1_32bit.exe")
        if run_test(
            "32-bit binary shellcode",
            f"{python_cmd} shcode2exe.py -o {output_file} test.bin",
            output_file,
            verify_shellcode="test.bin"
        ):
            tests_passed += 1
        
        # Test 2: String format shellcode (32-bit)
        tests_total += 1
        output_file = os.path.join(tmpdir, "test2_string.exe")
        if run_test(
            "32-bit string format shellcode",
            f"{python_cmd} shcode2exe.py -s -o {output_file} test.txt",
            output_file,
            verify_shellcode="test.bin"
        ):
            tests_passed += 1
        
        # Test 3: 64-bit binary shellcode
        tests_total += 1
        output_file = os.path.join(tmpdir, "test3_64bit.exe")
        if run_test(
            "64-bit binary shellcode",
            f"{python_cmd} shcode2exe.py -a 64 -o {output_file} test.bin",
            output_file,
            verify_shellcode="test.bin"
        ):
            tests_passed += 1
        
        # Test 4: Verbose mode
        tests_total += 1
        output_file = os.path.join(tmpdir, "test4_verbose.exe")
        if run_test(
            "Verbose mode output",
            f"{python_cmd} shcode2exe.py -V -o {output_file} test.bin",
            output_file,
            verify_shellcode="test.bin"
        ):
            tests_passed += 1
        
        # Test 5: Keep intermediate files
        tests_total += 1
        # For this test, we need to run in the current directory to find the intermediate files
        output_name = "test5_keep"
        output_file = output_name + ".exe"
        
        # Clean up any existing files first
        for ext in ['.exe', '.asm', '.obj']:
            if os.path.exists(output_name + ext):
                os.remove(output_name + ext)
        
        python_cmd = get_python_command()
        result = subprocess.run(
            f"{python_cmd} shcode2exe.py -k -o {output_file} test.bin",
            shell=True, capture_output=True, text=True
        )
        
        if result.returncode == 0 and os.path.exists(output_file):
            # Check if intermediate files were kept
            asm_file = f"{output_name}.asm"
            obj_file = f"{output_name}.obj"
            
            if os.path.exists(asm_file) and os.path.exists(obj_file):
                print(f"\n[TEST] Keep intermediate files")
                print(f"✅ PASSED: Intermediate files kept (.asm and .obj)")
                tests_passed += 1
                # Clean up
                for ext in ['.exe', '.asm', '.obj']:
                    if os.path.exists(output_name + ext):
                        os.remove(output_name + ext)
            else:
                print(f"\n[TEST] Keep intermediate files")
                print(f"❌ FAILED: Intermediate files not found")
                print(f"   Expected: {asm_file} and {obj_file}")
        else:
            print(f"\n[TEST] Keep intermediate files")
            print(f"❌ FAILED: Command failed")
    
    # Summary
    print(f"\n{'='*40}")
    print(f"Tests passed: {tests_passed}/{tests_total}")
    
    if tests_passed == tests_total:
        print("✅ All tests passed!")
        return 0
    else:
        print(f"❌ {tests_total - tests_passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())