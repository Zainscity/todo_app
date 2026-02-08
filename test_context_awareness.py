#!/usr/bin/env python3
"""
Test script for context-aware references in the Todo AI Chatbot.
This script validates that the AI can properly understand references
like "that task" or "the previous item" by using conversation history.
"""

import asyncio
import uuid
from sqlmodel import create_engine, Session, SQLModel
from backend.src.models.task_model import Task
from backend.src.models.conversation_model import Conversation
from backend.src.models.message_model import Message, Role
from backend.src.models.user import User
from backend.src.agents.todo_agent import TodoAgent
from backend.src.core.database import DATABASE_URL


def test_context_awareness():
    """
    Test that the AI can handle context-aware references like 'that task' or 'the previous item'.

    This test creates a simulated conversation where:
    1. User adds a task ("Buy groceries")
    2. User refers to "that task" and asks to complete it
    3. AI should understand that "that task" refers to the previously mentioned task
    """
    print("Testing context-aware references...")

    # Create a new conversation for testing
    user_id = f"test_user_{uuid.uuid4()}"

    # Create in-memory database for testing
    engine = create_engine("sqlite:///:memory:", echo=True)

    # Import all models to register them with SQLModel before creating tables
    from backend.src.models.user import User
    from backend.src.models.task_model import Task
    from backend.src.models.conversation_model import Conversation
    from backend.src.models.message_model import Message

    # Temporarily disable foreign key constraints to avoid the users table issue
    from sqlalchemy import text as sa_text
    with engine.begin() as conn:
        conn.execute(sa_text("PRAGMA foreign_keys=OFF"))
        # Now create all tables with foreign keys disabled
        SQLModel.metadata.create_all(conn)

    with Session(engine) as session:
        # Initialize the agent
        agent = TodoAgent()

        # Step 1: Add a task
        print("\nStep 1: Adding a task 'Buy groceries'")
        result1 = agent.process_request(
            user_id=user_id,
            user_message="Add a task to buy groceries",
            conversation_id=None,  # Will create new conversation
            db_session=session
        )

        print(f"Response: {result1['response']}")
        print(f"Tool calls: {len(result1['tool_calls'])}")

        # Extract the task ID from the tool call result
        task_id = None
        for tool_call in result1['tool_calls']:
            if tool_call['function']['name'] == 'add_task' and tool_call['function']['result'].get('success'):
                task = tool_call['function']['result'].get('task')
                if task:
                    task_id = task.get('id')
                    break

        if not task_id:
            print("ERROR: Could not extract task ID from add_task result")
            return False

        print(f"Created task with ID: {task_id}")

        # Create a conversation record for subsequent messages
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

        # Manually add the messages to the database to simulate the conversation
        user_msg1 = Message(
            user_id=user_id,
            conversation_id=conversation.id,
            role=Role.user,
            content="Add a task to buy groceries"
        )
        ai_msg1 = Message(
            user_id=user_id,
            conversation_id=conversation.id,
            role=Role.assistant,
            content=result1['response']
        )
        session.add(user_msg1)
        session.add(ai_msg1)
        session.commit()

        # Step 2: Refer to "that task" and complete it
        print(f"\nStep 2: Referring to 'that task' (ID: {task_id}) and completing it")
        print("User says: 'Complete that task'")

        result2 = agent.process_request(
            user_id=user_id,
            user_message="Complete that task",
            conversation_id=conversation.id,
            db_session=session
        )

        print(f"Response: {result2['response']}")
        print(f"Tool calls: {len(result2['tool_calls'])}")

        # Check if the AI called complete_task with the correct task_id
        success = False
        for tool_call in result2['tool_calls']:
            if tool_call['function']['name'] == 'complete_task':
                # Parse the arguments to check if it's trying to complete the right task
                import json
                args = json.loads(tool_call['function']['arguments'])
                called_task_id = args.get('task_id')

                if called_task_id == task_id:
                    print(f"SUCCESS: AI correctly identified 'that task' as task ID {task_id}")
                    success = True
                else:
                    print(f"FAILURE: AI tried to complete task ID {called_task_id}, but expected {task_id}")

        if not success:
            print("FAILURE: AI did not correctly interpret 'that task' in context")
            return False

        print("\nStep 3: Verify the task is completed")
        # Now let's check if the task was actually completed by listing tasks
        result3 = agent.process_request(
            user_id=user_id,
            user_message="List all my tasks",
            conversation_id=conversation.id,
            db_session=session
        )

        print(f"Response: {result3['response']}")

        # Add these messages to the conversation as well
        user_msg2 = Message(
            user_id=user_id,
            conversation_id=conversation.id,
            role=Role.user,
            content="Complete that task"
        )
        ai_msg2 = Message(
            user_id=user_id,
            conversation_id=conversation.id,
            role=Role.assistant,
            content=result2['response']
        )
        user_msg3 = Message(
            user_id=user_id,
            conversation_id=conversation.id,
            role=Role.user,
            content="List all my tasks"
        )
        ai_msg3 = Message(
            user_id=user_id,
            conversation_id=conversation.id,
            role=Role.assistant,
            content=result3['response']
        )
        session.add_all([user_msg2, ai_msg2, user_msg3, ai_msg3])
        session.commit()

        print("\nStep 4: Testing another context reference")
        # Step 4: Test another scenario - update "the previous task"
        print("Step 4: Updating 'the previous task' with a new description")
        print("User says: 'Update the previous task with description: important shopping'")

        result4 = agent.process_request(
            user_id=user_id,
            user_message="Update the previous task with description: important shopping",
            conversation_id=conversation.id,
            db_session=session
        )

        print(f"Response: {result4['response']}")

        # Check if the AI called update_task with the correct task_id
        success4 = False
        for tool_call in result4['tool_calls']:
            if tool_call['function']['name'] == 'update_task':
                import json
                args = json.loads(tool_call['function']['arguments'])
                called_task_id = args.get('task_id')

                if called_task_id == task_id:
                    print(f"SUCCESS: AI correctly identified 'the previous task' as task ID {task_id}")
                    success4 = True
                else:
                    print(f"FAILURE: AI tried to update task ID {called_task_id}, but expected {task_id}")

        if not success4:
            print("FAILURE: AI did not correctly interpret 'the previous task' in context")
            return False

        print("\n✅ Context awareness test passed!")
        print("- AI correctly understood 'that task' to refer to the previously mentioned task")
        print("- AI correctly understood 'the previous task' to refer to the most recent task")
        print("- Conversation history was properly maintained and used for context")

        return True


def run_test():
    """Run the context awareness test."""
    print("=" * 60)
    print("TODO AI CHATBOT - CONTEXT AWARENESS TEST")
    print("=" * 60)

    try:
        success = test_context_awareness()
        if success:
            print("\n🎉 ALL TESTS PASSED! Context-aware references are working correctly.")
            return True
        else:
            print("\n❌ TESTS FAILED! Context-aware references need fixing.")
            return False
    except Exception as e:
        print(f"\n💥 ERROR RUNNING TEST: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    run_test()