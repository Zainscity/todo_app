#!/usr/bin/env python3
"""
Test script for handling partial information requests in the Todo AI Chatbot.
This test validates that the system properly handles requests like
"change the task" with partial information by asking for clarification.
"""

import os
import sys
from unittest.mock import Mock, patch
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Mock the OpenAI client before importing TodoAgent
original_openai = __import__('openai', fromlist=['OpenAI'])

mock_openai = Mock()
mock_client = Mock()
mock_completion = Mock()
mock_choice = Mock()
mock_choice.message = Mock()
mock_choice.message.tool_calls = []
mock_choice.message.content = "Mock response"
mock_completion.choices = [mock_choice]
mock_client.chat.completions.create.return_value = mock_completion
mock_openai.OpenAI.return_value = mock_client

# Temporarily replace the openai module
import builtins
_original_import = builtins.__import__

def _mock_import(name, *args, **kwargs):
    if name == 'openai':
        return mock_openai
    return _original_import(name, *args, **kwargs)

builtins.__import__ = _mock_import

try:
    from backend.src.agents.todo_agent import TodoAgent
finally:
    # Restore original import
    builtins.__import__ = _original_import

# Set a fake API key for testing to avoid initialization issues
os.environ['OPENAI_API_KEY'] = 'fake-key-for-testing'


def test_partial_information_detection():
    """
    Test the detection of partial information requests that need clarification.
    """
    print("Testing partial information request detection...")

    agent = TodoAgent()

    # Test cases for partial information requests that should ask for clarification
    partial_info_requests = [
        "change the task",
        "modify the task",
        "update the task",
        "complete the task",
        "delete the task",
        "finish the task",
        "redo the task",
        "adjust the task",
        "tweak the task",
        "work on the task",
        "deal with that task",
        "handle the task",
        "address the task"
    ]

    success_count = 0
    total_count = len(partial_info_requests)

    for request in partial_info_requests:
        print(f"  Testing: '{request}'")

        is_ambiguous, clarification = agent._detect_ambiguity(request)

        if is_ambiguous:
            print(f"    ✅ Correctly identified as requiring clarification: {clarification}")
            success_count += 1
        else:
            print(f"    ❌ Should have been identified as needing clarification")

    print(f"\nPartial information detection: {success_count}/{total_count} passed")
    return success_count == total_count


def test_contextual_partial_info():
    """
    Test that requests remain ambiguous even with some context but still lack specifics.
    """
    print("\nTesting contextual partial information requests...")

    agent = TodoAgent()

    # Requests that have some context but still lack specific task information
    contextual_requests = [
        "change that task",
        "update this task",
        "modify such and such task",
        "complete tasks",
        "delete task items",
        "work on my task",
        "handle the thing",
        "fix the thing"
    ]

    success_count = 0
    total_count = len(contextual_requests)

    for request in contextual_requests:
        print(f"  Testing: '{request}'")

        is_ambiguous, clarification = agent._detect_ambiguity(request)

        if is_ambiguous:
            print(f"    ✅ Correctly identified as ambiguous: {clarification}")
            success_count += 1
        else:
            print(f"    ❌ Should have been identified as ambiguous")

    print(f"\nContextual partial info detection: {success_count}/{total_count} passed")
    return success_count == total_count


def test_specific_requests_still_work():
    """
    Test that specific requests are not flagged as ambiguous.
    """
    print("\nTesting that specific requests are not flagged as ambiguous...")

    agent = TodoAgent()

    # Specific requests that should NOT be flagged as ambiguous
    specific_requests = [
        "complete task 1",
        "update task 5 with new description",
        "delete task 3",
        "add a new task to buy milk",
        "list all tasks",
        "mark task 10 as complete",
        "show pending tasks",
        "rename task 2 to 'new title'"
    ]

    success_count = 0
    total_count = len(specific_requests)

    for request in specific_requests:
        print(f"  Testing: '{request}'")

        is_ambiguous, clarification = agent._detect_ambiguity(request)

        if not is_ambiguous:
            print(f"    ✅ Correctly identified as not ambiguous")
            success_count += 1
        else:
            print(f"    ❌ Should NOT have been identified as ambiguous: {clarification}")

    print(f"\nSpecific requests detection: {success_count}/{total_count} passed")
    return success_count == total_count


def test_full_process_with_partial_info():
    """
    Test the full process_request flow with partial information using mocks.
    """
    print("\nTesting full process_request flow with partial information...")

    agent = TodoAgent()

    # Test partial information request
    with patch.object(agent, '_detect_ambiguity') as mock_detect:
        mock_detect.return_value = (True, "Could you clarify which task you mean? Please specify the task title or ID.")

        result = agent.process_request(
            user_id="test_user_123",
            user_message="change the task",
            conversation_history=[],
            conversation_id=None,
            db_session=None
        )

        print(f"  Input: 'change the task'")
        print(f"  Response: '{result['response']}'")
        print(f"  Tool calls: {len(result['tool_calls'])}")
        print(f"  Success: {result['success']}")

        if (result['response'] == "Could you clarify which task you mean? Please specify the task title or ID." and
            len(result['tool_calls']) == 0 and
            result['success'] == True):
            print(f"  ✅ Partial information request handled correctly - no tool calls, proper clarification")
            return True
        else:
            print(f"  ❌ Partial information request not handled correctly")
            return False


def run_tests():
    """Run all partial information handling tests."""
    print("=" * 60)
    print("TODO AI CHATBOT - PARTIAL INFORMATION REQUESTS HANDLING TESTS")
    print("=" * 60)

    test1_passed = test_partial_information_detection()
    test2_passed = test_contextual_partial_info()
    test3_passed = test_specific_requests_still_work()
    test4_passed = test_full_process_with_partial_info()

    print(f"\n{'='*60}")
    print("FINAL RESULTS:")
    print(f"Partial info detection test: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Contextual partial info test: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    print(f"Specific requests test: {'✅ PASSED' if test3_passed else '❌ FAILED'}")
    print(f"Full process test: {'✅ PASSED' if test4_passed else '❌ FAILED'}")

    overall_success = all([test1_passed, test2_passed, test3_passed, test4_passed])
    print(f"\nOverall: {'🎉 ALL TESTS PASSED!' if overall_success else '❌ SOME TESTS FAILED!'}")

    return overall_success


if __name__ == "__main__":
    run_tests()