---
id: 13
title: Fix Generator Context Manager TypeError in Chatbot Tool Functions
stage: green
date: 2026-02-08
user: zainscity
model: 
  - gemini-1.5-pro
feature: ai-chatbot
description: Fix `TypeError: 'generator' object does not support the context manager protocol` by replacing the `get_session` generator with the `get_session_context` context manager in all chatbot tool functions.
architecture-decisions:
  - ADR-001: Tool Calling for Chatbot Interaction
---

## Prompt

"input (add grocery to tasks) output (It seems like there was an error with the tool call. The 'generator' object does not support the context manager protocol is usually a sign that the code was trying to use a generator object in a way that's not compatible with its design...)"

## Details

After resolving the `user_id` context issue, a new error was reported by the chatbot: `TypeError: 'generator' object does not support the context manager protocol`. This indicated a problem within the Python code of the tool functions, specifically around the `with` statement used for database sessions.

An investigation of `backend/src/models/database.py` revealed that the `get_session` function, used by all tool functions in `chatbot_service.py`, was a generator function (using `yield`) but was not decorated with `@contextmanager`. This caused the `with` statement to fail. The same file contained a `get_session_context` function which was a proper context manager with transaction handling (commit/rollback/close).

## Fix

The `backend/src/services/chatbot_service.py` file was modified to use the correct context manager for database sessions.

1.  **Imported `get_session_context`**: The `get_session_context` function was imported from `..models.database`.
2.  **Replaced `get_session` with `get_session_context`**: All four occurrences of `with get_session() as session:` in the tool functions (`create_task_tool`, `get_tasks_tool`, `update_task_tool`, `delete_task_tool`) were replaced with `with get_session_context() as session:`.

This ensures that a proper database session with correct transaction management is used for all tool-related database operations, resolving the `TypeError`.

## Files Modified

- `backend/src/services/chatbot_service.py`

## Tests

No new tests were written. Manual verification is needed to confirm that the chatbot can now successfully create, read, update, and delete tasks without encountering the context manager `TypeError`.
