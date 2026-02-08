# Context Awareness Test for Todo AI Chatbot

This test validates that the Todo AI Chatbot can handle context-aware references such as "that task" or "the previous item" by leveraging conversation history.

## Test Coverage

The test verifies that:

1. **System Prompt Contains Context Instructions**: The AI receives instructions about handling context-aware references like "that task" and "the previous one".

2. **Conversation History Included**: Previous conversation messages are properly included in the AI request context.

3. **Reference Resolution**: The AI can potentially map contextual references to specific task IDs when appropriate context is provided.

## Test Methodology

The test uses mocking to validate the agent's behavior without requiring actual AI API calls or database operations. It focuses on the architectural aspects that enable context awareness:

- Verifies the system prompt includes context-aware instructions
- Checks that conversation history is passed to the AI
- Validates that the agent can process contextual references to tasks

## Files Created

- `test_context_awareness_simple.py`: Main test implementation
- This README file

## Implementation Status

The TodoAgent implementation properly supports context-aware references through:
- System prompt instructions for handling contextual references
- Proper inclusion of conversation history in AI requests
- Tool call mechanism to act on resolved task references