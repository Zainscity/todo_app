#!/usr/bin/env python3
"""
Test script for handling ambiguous requests in the Todo AI Chatbot.
This test validates that the system properly handles requests like
"complete a task" without specification by asking for clarification.
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Set a fake API key for testing to avoid initialization issues
os.environ['OPENAI_API_KEY'] = 'fake-key-for-testing'

from backend.src.agents.todo_agent import TodoAgent


def test_ambiguous_requests():
    """
    Test various ambiguous requests that should trigger clarification.
    """
    print("Testing handling of ambiguous requests...")

    agent = TodoAgent()

    # Test cases for ambiguous requests that should ask for clarification
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
        "complete task",
        "delete task",
        "update task"
    ]

    success_count = 0
    total_count = len(ambiguous_requests)

    for request in ambiguous_requests:
        print(f"\nTesting: '{request}'")

        result = agent.process_request(
            user_id="test_user_123",
            user_message=request,
            conversation_history=[],
            conversation_id=None,
            db_session=None
        )

        # Check that no tool calls were made (since it's ambiguous)
        if len(result['tool_calls']) == 0:
            print(f"  ✅ No tool calls made (correct)")

            # Check that the response asks for clarification
            response_lower = result['response'].lower()
            if any(keyword in response_lower for keyword in ['which', 'specific', 'clarify', 'please', 'specify', 'task']):
                print(f"  ✅ Response asks for clarification: '{result['response']}'")
                success_count += 1
            else:
                print(f"  ❌ Response doesn't ask for clarification: '{result['response']}'")
        else:
            print(f"  ❌ Tool calls were made, but request was ambiguous: {result['tool_calls']}")

    print(f"\n{'='*60}")
    print(f"AMBIGUOUS REQUESTS TEST RESULTS:")
    print(f"Passed: {success_count}/{total_count}")
    print(f"Success rate: {success_count/total_count*100:.1f}%")

    return success_count == total_count


def test_non_ambiguous_requests():
    """
    Test that non-ambiguous requests still work correctly.
    """
    print(f"\n{'-'*60}")
    print("Testing non-ambiguous requests (should work normally)...")

    agent = TodoAgent()

    # Test cases for non-ambiguous requests that should be processed normally
    non_ambiguous_requests = [
        ("add a task to buy groceries", ["add_task"]),
        ("list my tasks", ["list_tasks"]),
        ("complete task 1", ["complete_task"]),
        ("delete task 5", ["delete_task"]),
        ("update task 3 with new description", ["update_task"])
    ]

    success_count = 0
    total_count = len(non_ambiguous_requests)

    for request, expected_tools in non_ambiguous_requests:
        print(f"\nTesting: '{request}' (should trigger: {expected_tools})")

        # Mock the OpenAI response to simulate tool calls
        import json
        from unittest.mock import Mock, patch

        mock_tool_call = Mock()
        mock_tool_call.id = "call_abc123"
        mock_tool_call.function = Mock()
        mock_tool_call.function.name = expected_tools[0] if expected_tools else "add_task"
        mock_tool_call.function.arguments = '{"title": "test"}' if expected_tools[0] == "add_task" else '{"task_id": 1}'

        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message = Mock()
        mock_response.choices[0].message.tool_calls = [mock_tool_call] if expected_tools else []
        mock_response.choices[0].message.content = None

        with patch.object(agent.client.chat.completions, 'create', return_value=mock_response):
            # Also mock the MCP service call
            mcp_method_map = {
                "add_task": "call_add_task",
                "list_tasks": "call_list_tasks",
                "complete_task": "call_complete_task",
                "delete_task": "call_delete_task",
                "update_task": "call_update_task"
            }

            mcp_method_name = mcp_method_map.get(expected_tools[0], "call_add_task")
            mcp_mock_attrs = {mcp_method_name: lambda **kwargs: {"success": True, "task": {"id": 1, "title": "test"}}}

            with patch.object(agent.mcp_service, **mcp_mock_attrs):
                result = agent.process_request(
                    user_id="test_user_123",
                    user_message=request,
                    conversation_history=[],
                    conversation_id=None,
                    db_session=None
                )

                # For non-ambiguous requests, we expect tool calls to be made
                if len(result['tool_calls']) > 0:
                    print(f"  ✅ Tool calls made (correct)")
                    print(f"  ✅ Request processed normally")
                    success_count += 1
                else:
                    print(f"  ❌ No tool calls made, but request was clear: {result['tool_calls']}")

    print(f"\n{'='*60}")
    print(f"NON-AMBIGUOUS REQUESTS TEST RESULTS:")
    print(f"Passed: {success_count}/{total_count}")
    print(f"Success rate: {success_count/total_count*100:.1f}%")

    return success_count == total_count


def test_conversation_context_with_clarifications():
    """
    Test that clarifications work in conversation context.
    """
    print(f"\n{'-'*60}")
    print("Testing clarifications in conversation context...")

    agent = TodoAgent()

    # Simulate a conversation where user gives ambiguous request after getting task list
    conversation_history = [
        {"role": "user", "content": "list my tasks"},
        {"role": "assistant", "content": "You have 2 tasks: 1. Buy groceries 2. Call mom"}
    ]

    # Now user says "complete that task" - should ask for clarification since multiple tasks exist
    result = agent.process_request(
        user_id="test_user_123",
        user_message="complete that task",
        conversation_history=conversation_history,
        conversation_id=None,
        db_session=None
    )

    print(f"Input in context: 'complete that task'")
    print(f"Response: '{result['response']}'")

    # Should ask for clarification about which task
    if len(result['tool_calls']) == 0:
        print("✅ No tool calls made for ambiguous reference")

        response_lower = result['response'].lower()
        if any(keyword in response_lower for keyword in ['which', 'specific', 'clarify', 'please', 'specify']):
            print("✅ Response asks for clarification in context")
            print("✅ Conversation context handling works correctly")
            return True
        else:
            print("❌ Response doesn't ask for clarification properly")
            return False
    else:
        print("❌ Tool calls made despite ambiguous reference in context")
        return False


def run_tests():
    """Run all ambiguous request tests."""
    print("=" * 60)
    print("TODO AI CHATBOT - AMBIGUOUS REQUESTS HANDLING TESTS")
    print("=" * 60)

    test1_passed = test_ambiguous_requests()
    test2_passed = test_non_ambiguous_requests()
    test3_passed = test_conversation_context_with_clarifications()

    print(f"\n{'='*60}")
    print("FINAL RESULTS:")
    print(f"Ambiguous requests test: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Non-ambiguous requests test: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    print(f"Context with clarifications test: {'✅ PASSED' if test3_passed else '❌ FAILED'}")

    overall_success = test1_passed and test2_passed and test3_passed
    print(f"\nOverall: {'🎉 ALL TESTS PASSED!' if overall_success else '❌ SOME TESTS FAILED!'}")

    return overall_success


if __name__ == "__main__":
    run_tests()