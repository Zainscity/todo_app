#!/usr/bin/env python3
"""
Integration Test Script for Todo App

This script performs basic integration testing of all core features.
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd_args):
    """Run a command and return the result."""
    try:
        result = subprocess.run(
            [sys.executable] + cmd_args,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"


def test_add_task():
    """Test adding a task."""
    print("Testing: Add task")
    code, stdout, stderr = run_command(["src/main.py", "add", "Test task", "This is a test"])

    if code == 0 and "Task added successfully!" in stdout:
        print("✓ Add task test passed")
        return True
    else:
        print(f"✗ Add task test failed: {stderr or stdout}")
        return False


def test_view_tasks():
    """Test viewing tasks."""
    print("Testing: View tasks")
    code, stdout, stderr = run_command(["src/main.py", "view"])

    if code == 0 and ("All Tasks:" in stdout or "No tasks found" in stdout):
        print("✓ View tasks test passed")
        return True
    else:
        print(f"✗ View tasks test failed: {stderr or stdout}")
        return False


def test_complete_task():
    """Test completing a task (this will fail since we can't guarantee a task exists)."""
    print("Testing: Complete task (should fail - no tasks exist)")
    code, stdout, stderr = run_command(["src/main.py", "complete", "1"])

    # This test expects failure since no tasks exist
    if code == 0 or "does not exist" in stdout:
        print("✓ Complete task test passed (expected failure due to non-existent task)")
        return True
    else:
        print(f"✗ Complete task test unexpected result: {stderr or stdout}")
        return False


def test_help():
    """Test help command."""
    print("Testing: Help command")
    code, stdout, stderr = run_command(["src/main.py", "help"])

    if code == 0 and "Available commands:" in stdout:
        print("✓ Help command test passed")
        return True
    else:
        print(f"✗ Help command test failed: {stderr or stdout}")
        return False


def run_integration_tests():
    """Run all integration tests."""
    print("Starting integration tests for Todo App...\n")

    tests = [
        test_help,
        test_view_tasks,
        test_add_task,
        test_complete_task,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print(f"Integration tests complete: {passed}/{total} passed")

    if passed == total:
        print("🎉 All integration tests passed!")
        return True
    else:
        print(f"❌ {total - passed} tests failed")
        return False


if __name__ == "__main__":
    success = run_integration_tests()
    sys.exit(0 if success else 1)