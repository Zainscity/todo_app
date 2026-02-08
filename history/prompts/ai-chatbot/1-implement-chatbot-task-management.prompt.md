---
id: 1
title: Implement Chatbot Task Management
stage: implement
date: 2026-02-08
user: zainscity
model: 
  - gemini-1.5-pro
feature: ai-chatbot
description: Implement functionality for the chatbot to add, view, update, and delete tasks by integrating with existing task services via tool calling.
architecture-decisions:
  - ADR-001: Tool Calling for Chatbot Interaction
---

## Prompt

the chatbot is functional and replying to the chat, but I want to add a functionality, When I ask the chatbot to add a task it should add tasks.

## Details

The user requested to extend the chatbot's capabilities to include task management. Specifically, the chatbot should be able to create tasks when instructed by the user.

## Changes

The `backend/src/services/chatbot_service.py` file was modified to incorporate tool calling. This involved:

1.  **Defining Tool Specifications**: Added JSON schema definitions for `create_task_tool`, `get_tasks_tool`, `update_task_tool`, and `delete_task_tool`.
2.  **Modifying `get_chatbot_response`**:
    *   The `external_client.chat.completions.create` function now receives the `tools` definitions and `tool_choice="auto"`.
    *   Logic was added to detect `tool_calls` from the LLM's response.
    *   An `available_functions` dictionary maps tool names to their corresponding Python functions.
    *   When a tool call is detected, the appropriate function is executed with arguments parsed from the LLM's `tool_call.function.parameters`.
    *   The `user_id` is passed to the tool functions, with a fallback to the `user_id` from the initial chat request if not provided by the LLM.
    *   The output of the tool execution is then sent back to the LLM to generate a final natural language response to the user.
    *   If no tool call is made, the LLM's direct response is returned.

## Files Modified

- `backend/src/services/chatbot_service.py`

## Tests

No new tests were written as part of this change. The existing tests for the chatbot and task services should cover the underlying functionality. Integration tests specific to the chatbot's tool-calling capability would be beneficial but are outside the scope of this immediate request.

## Future Considerations

- Adding specific unit tests for the tool-calling logic in `chatbot_service.py`.
- Improving error handling and user feedback for tool execution failures.
- Expanding the toolset to include other task-related operations (e.g., mark task complete/incomplete).
- Implementing more sophisticated natural language understanding for extracting task details.
