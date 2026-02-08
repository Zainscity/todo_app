#!/usr/bin/env python3
"""
Test script for ambiguity detection in the Todo AI Chatbot.
This test verifies that the TodoAgent can detect ambiguous requests
and ask for clarification instead of guessing.
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Set a fake API key for testing to avoid initialization issues
os.environ['OPENAI_API_KEY'] = 'fake-key-for-testing'

from backend.src.agents.todo_agent import TodoAgent


def test_ambiguity_detection():
    """
    Test that the TodoAgent can detect ambiguous requests and ask for clarification.
    """
    print("Testing ambiguity detection in TodoAgent...")

    # Initialize the agent
    agent = TodoAgent()

    # Test cases for ambiguous requests
    test_cases = [
        {
            "input": "Complete that task",
            "should_be_ambiguous": True,
            "expected_part": "clarify"
        },
        {
            "input": "Delete that task",
            "should_be_ambiguous": True,
            "expected_part": "specific"
        },
        {
            "input": "Update the task",
            "should_be_ambiguous": True,
            "expected_part": "specific"
        },
        {
            "input": "Change that task",
            "should_be_ambiguous": True,
            "expected_part": "specific"
        },
        {
            "input": "Complete task 1",
            "should_be_ambiguous": False,
            "expected_part": None  # Should not trigger ambiguity detection
        },
        {
            "input": "Add a task to buy groceries",
            "should_be_ambiguous": False,
            "expected_part": None  # Should not trigger ambiguity detection
        }
    ]

    all_tests_passed = True

    for i, test_case in enumerate(test_cases):
        input_msg = test_case["input"]
        should_be_ambiguous = test_case["should_be_ambiguous"]

        print(f"\nTest {i+1}: Input: '{input_msg}'")

        # Use the internal method to test ambiguity detection directly
        is_ambiguous, clarification = agent._detect_ambiguity(input_msg)

        print(f"  Detected as ambiguous: {is_ambiguous}")
        print(f"  Clarification needed: {clarification}")

        if should_be_ambiguous:
            if is_ambiguous:
                print(f"  ✅ Correctly identified as ambiguous")
                if test_case["expected_part"] and test_case["expected_part"] in clarification.lower():
                    print(f"  ✅ Clarification question is appropriate")
                else:
                    print(f"  ⚠️  Clarification question could be improved")
            else:
                print(f"  ❌ Should have been detected as ambiguous")
                all_tests_passed = False
        else:
            if not is_ambiguous:
                print(f"  ✅ Correctly identified as not ambiguous")
            else:
                print(f"  ❌ Should NOT have been detected as ambiguous")
                all_tests_passed = False

    print(f"\n{'='*60}")
    if all_tests_passed:
        print("✅ AMBIGUITY DETECTION TESTS PASSED!")
        print("The TodoAgent correctly identifies ambiguous requests and asks for clarification.")
    else:
        print("❌ SOME AMBIGUITY DETECTION TESTS FAILED!")
        print("The TodoAgent needs improvement in detecting ambiguous requests.")

    return all_tests_passed


def test_full_process_with_ambiguous_input():
    """
    Test the full process_request method with an ambiguous input.
    """
    print(f"\n{'='*60}")
    print("Testing full process_request with ambiguous input...")

    agent = TodoAgent()

    # Test an ambiguous request
    result = agent.process_request(
        user_id="test_user_123",
        user_message="Complete that task",
        conversation_history=[],
        conversation_id=None,
        db_session=None
    )

    print(f"Input: 'Complete that task'")
    print(f"Response: '{result['response']}'")
    print(f"Success: {result['success']}")
    print(f"Tool calls made: {len(result['tool_calls'])}")

    # Verify that no tool calls were made (since it's ambiguous)
    if len(result['tool_calls']) == 0:
        print("✅ No tool calls made for ambiguous request (correct behavior)")
    else:
        print("❌ Tool calls were made for ambiguous request (incorrect behavior)")
        return False

    # Verify that the response asks for clarification
    response_lower = result['response'].lower()
    if any(word in response_lower for word in ['clarify', 'specific', 'which', 'please']):
        print("✅ Response asks for clarification (correct behavior)")
        return True
    else:
        print("❌ Response does not ask for clarification (incorrect behavior)")
        return False


def run_tests():
    """Run all ambiguity detection tests."""
    print("=" * 60)
    print("TODO AI CHATBOT - AMBIGUITY DETECTION TESTS")
    print("=" * 60)

    test1_passed = test_ambiguity_detection()
    test2_passed = test_full_process_with_ambiguous_input()

    print(f"\n{'='*60}")
    print("FINAL RESULTS:")
    print(f"Ambiguity detection tests: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Full process tests: {'✅ PASSED' if test2_passed else '❌ FAILED'}")

    overall_success = test1_passed and test2_passed
    print(f"Overall: {'🎉 ALL TESTS PASSED!' if overall_success else '❌ SOME TESTS FAILED!'}")

    return overall_success


if __name__ == "__main__":
    run_tests()