#!/usr/bin/env python3
"""
Simple test for handling ambiguous requests in the Todo AI Chatbot.
This test validates the ambiguity detection logic directly without API calls.
"""

import os
import sys
from unittest.mock import Mock, patch, MagicMock
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


def test_ambiguity_detection_logic():
    """
    Test the internal ambiguity detection logic directly.
    """
    print("Testing ambiguity detection logic directly...")

    agent = TodoAgent()

    # Test cases for ambiguous requests that should trigger clarification
    ambiguous_requests = [
        "complete a task",
        "delete a task",
        "update a task",
        "change a task",
        "modify a task",
        "complete the task",
        "delete the task",
        "update the task",
        "complete that task",
        "delete that task",
        "update this task",
        "complete task",  # This one is vague without a number
        "delete task",    # This one is vague without a number
        "update task"     # This one is vague without a number
    ]

    success_count = 0
    total_count = len(ambiguous_requests)

    for request in ambiguous_requests:
        print(f"  Testing: '{request}'")

        is_ambiguous, clarification = agent._detect_ambiguity(request)

        if is_ambiguous:
            print(f"    ✅ Correctly identified as ambiguous: {clarification}")
            success_count += 1
        else:
            print(f"    ❌ Should have been identified as ambiguous")

    print(f"\nAmbiguity detection: {success_count}/{total_count} passed")
    return success_count == total_count


def test_non_ambiguous_requests():
    """
    Test that non-ambiguous requests are not flagged as ambiguous.
    """
    print("\nTesting non-ambiguous requests...")

    agent = TodoAgent()

    # Test cases for non-ambiguous requests that should NOT trigger ambiguity
    non_ambiguous_requests = [
        "complete task 1",
        "delete task 2",
        "update task 3 with new description",
        "add a task to buy groceries",
        "list my tasks",
        "complete task 100",
        "add task wash dishes",
        "show pending tasks"
    ]

    success_count = 0
    total_count = len(non_ambiguous_requests)

    for request in non_ambiguous_requests:
        print(f"  Testing: '{request}'")

        is_ambiguous, clarification = agent._detect_ambiguity(request)

        if not is_ambiguous:
            print(f"    ✅ Correctly identified as not ambiguous")
            success_count += 1
        else:
            print(f"    ❌ Should NOT have been identified as ambiguous: {clarification}")

    print(f"\nNon-ambiguous detection: {success_count}/{total_count} passed")
    return success_count == total_count


def test_ambiguous_process_flow():
    """
    Test the full process_request flow for ambiguous requests using mocks.
    """
    print("\nTesting full process_request flow for ambiguous requests...")

    agent = TodoAgent()

    # Test ambiguous request with mocked API calls
    with patch.object(agent, '_detect_ambiguity') as mock_detect:
        mock_detect.return_value = (True, "Which task would you like to complete?")

        result = agent.process_request(
            user_id="test_user_123",
            user_message="complete that task",
            conversation_history=[],
            conversation_id=None,
            db_session=None
        )

        print(f"  Input: 'complete that task'")
        print(f"  Response: '{result['response']}'")
        print(f"  Tool calls: {len(result['tool_calls'])}")
        print(f"  Success: {result['success']}")

        if (result['response'] == "Which task would you like to complete?" and
            len(result['tool_calls']) == 0 and
            result['success'] == True):
            print(f"  ✅ Ambiguous request handled correctly - no tool calls, proper clarification")
            return True
        else:
            print(f"  ❌ Ambiguous request not handled correctly")
            return False


def test_normal_process_flow():
    """
    Test the full process_request flow for non-ambiguous requests using mocks.
    """
    print("\nTesting full process_request flow for non-ambiguous requests...")

    agent = TodoAgent()

    # Mock the OpenAI response
    mock_response = Mock()
    mock_choice = Mock()
    mock_choice.message = Mock()
    mock_choice.message.tool_calls = []  # For simplicity, no tool calls in this test
    mock_choice.message.content = "I've added your task."
    mock_response.choices = [mock_choice]

    with patch.object(agent, '_detect_ambiguity') as mock_detect:
        mock_detect.return_value = (False, "")
        with patch.object(agent.client.chat.completions, 'create', return_value=mock_response):
            result = agent.process_request(
                user_id="test_user_123",
                user_message="add a task to buy groceries",
                conversation_history=[],
                conversation_id=None,
                db_session=None
            )

            print(f"  Input: 'add a task to buy groceries'")
            print(f"  Response: '{result['response']}'")
            print(f"  Success: {result['success']}")

            # For non-ambiguous requests, it should continue to process normally
            # (the actual processing depends on the AI response, which we've mocked)
            if result['success'] == True:
                print(f"  ✅ Non-ambiguous request processed normally")
                return True
            else:
                print(f"  ❌ Non-ambiguous request not processed correctly")
                return False


def run_tests():
    """Run all ambiguous request tests."""
    print("=" * 60)
    print("TODO AI CHATBOT - AMBIGUOUS REQUESTS HANDLING TESTS (SIMPLE)")
    print("=" * 60)

    test1_passed = test_ambiguity_detection_logic()
    test2_passed = test_non_ambiguous_requests()
    test3_passed = test_ambiguous_process_flow()
    test4_passed = test_normal_process_flow()

    print(f"\n{'='*60}")
    print("FINAL RESULTS:")
    print(f"Ambiguity detection logic test: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Non-ambiguous requests test: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    print(f"Ambiguous process flow test: {'✅ PASSED' if test3_passed else '❌ FAILED'}")
    print(f"Normal process flow test: {'✅ PASSED' if test4_passed else '❌ FAILED'}")

    overall_success = all([test1_passed, test2_passed, test3_passed, test4_passed])
    print(f"\nOverall: {'🎉 ALL TESTS PASSED!' if overall_success else '❌ SOME TESTS FAILED!'}")

    return overall_success


if __name__ == "__main__":
    run_tests()