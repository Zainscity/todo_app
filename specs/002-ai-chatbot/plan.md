# Implementation Plan: AI-Powered Todo Chatbot

**Feature Branch**: `002-ai-chatbot`  
**Created**: 2026-02-07  
**Status**: Draft

## 1. Technical Context

### 1.1. Overview
This plan details the implementation of an AI-powered chatbot for the existing Todo application. The chatbot will allow users to manage their tasks through natural language conversations, leveraging the OpenAI Agents SDK for reasoning and tool execution.

### 1.2. Tech Stack
-   **Backend**: Python FastAPI
-   **AI Agent Framework**: OpenAI Agents SDK
-   **Database**: PostgreSQL (via SQLModel ORM)
-   **Authentication**: Better Auth (JWT-based)
-   **Frontend**: Next.js (for integration of a chat UI)

### 1.3. Architecture
The chatbot will be integrated into the existing FastAPI backend. User requests from the frontend chat UI will be forwarded to a new backend endpoint. This endpoint will interact with the OpenAI Agents SDK, which will then use defined tools to perform CRUD operations on tasks in the PostgreSQL database. The server remains stateless, with all conversational history and task data persisted in the database.

### 1.4. Key Components
-   **Chatbot API Endpoint**: A new FastAPI endpoint to receive user messages and return chatbot responses.
-   **Chatbot Service**: A Python service responsible for orchestrating the OpenAI Agent, defining its tools, and managing conversation state.
-   **OpenAI Agent**: Configured with access to task management tools.
-   **Task Management Tools**: Functions/classes that wrap existing `task_service` operations (create, read, update, delete tasks).
-   **Chat UI Component**: A new React component in the Next.js frontend to display the chat interface.

### 1.5. Data Model Extensions
-   **ChatbotSession**: To store conversation history and context for each user.
    -   `session_id` (UUID, primary key)
    -   `user_id` (UUID, foreign key to User)
    -   `conversation_history` (JSONB or similar, array of messages)
    -   `created_at` (DateTime)
    -   `updated_at` (DateTime)
-   **ToolCallLog (Optional for auditability)**: To log agent's tool usage.
    -   `log_id` (UUID, primary key)
    -   `session_id` (UUID, foreign key to ChatbotSession)
    -   `tool_name` (String)
    -   `parameters` (JSONB)
    -   `result` (JSONB)
    -   `timestamp` (DateTime)

## 2. Constitution Check

### 2.1. Core Principles
-   **Spec-Driven Development Only**: ✅ This plan is derived directly from the `spec.md`.
-   **No Manual Code Writing**: ✅ All implementation will be driven by agent commands and generated code.
-   **Stateless Server Architecture**: ✅ The design maintains a stateless server; conversation state is externalized to the `ChatbotSession` in the database.
-   **Database is the Single Source of Truth**: ✅ All task and conversation data will be persisted in PostgreSQL.
-   **Tools Must Be Deterministic and Idempotent**: ✅ Task CRUD operations are inherently idempotent where applicable (e.g., updating a task to the same state). New tools will be designed with determinism in mind.

### 2.2. Architecture Rules
-   **FastAPI handles HTTP only**: ✅ The new API endpoint will only handle HTTP, delegating chatbot logic to a dedicated service.
-   **OpenAI Agents SDK handles reasoning**: ✅ Explicitly stated as the framework for agent logic.

### 2.3. Behavior Rules
-   **Agent must confirm all successful actions**: ✅ Responses will be structured to include success confirmations.
-   **Errors must be handled gracefully and explained**: ✅ Error handling will be implemented to provide clear explanations.
-   **No hallucinated task data**: ✅ Chatbot will only retrieve and manipulate data from the database via defined tools.
-   **Tool usage must be logged and returned in response**: ✅ The `ToolCallLog` entity (if implemented) and agent's response structure will support this.

### 2.4. Security Rules
-   **All operations are scoped by user_id**: ✅ All task operations via the chatbot will be implicitly scoped by the authenticated user's ID. `ChatbotSession` is also `user_id`-scoped.
-   **Authentication handled via Better Auth**: ✅ The FastAPI endpoint will use existing Better Auth mechanisms.
-   **No cross-user data leakage**: ✅ Enforced by `user_id` scoping.

### 2.5. Judging Criteria
-   **Correct use of OpenAI Agents SDK**: ✅ Central to the implementation.
-   **Clean stateless request cycle**: ✅ Design adheres to this.
-   **Accurate natural language → tool mapping**: ✅ A primary focus of agent configuration.
-   **Clear separation of concerns**: ✅ Achieved by dedicated API, service, and tool layers.

### 2.6. Disallowed
-   **Manual code edits**: ✅ Will be avoided.
-   **Skipping Spec-Kit steps**: ✅ All steps are being followed.
-   **Business logic inside frontend**: ✅ Frontend will only be a UI client for the chatbot API.

## 3. Implementation Plan

### Phase 1: Backend Chatbot API & Service

**Goal**: Establish the core chatbot logic and expose it via a FastAPI endpoint.

1.  **Environment Setup**:
    -   Install OpenAI Agents SDK in the backend environment.
    -   Ensure necessary environment variables for OpenAI API are configured.
2.  **Data Model Implementation**:
    -   Define `ChatbotSession` SQLModel.
    -   Define `ToolCallLog` SQLModel (optional, based on auditability needs).
    -   Run Alembic migrations to update the database schema.
3.  **Task Management Tools Development**:
    -   Create Python functions/classes that wrap existing `task_service` functions (e.g., `create_task_tool`, `get_tasks_tool`, `update_task_tool`, `delete_task_tool`). These will serve as the tools for the OpenAI Agent.
    -   Ensure these tools are properly decorated/formatted for the OpenAI Agents SDK.
4.  **Chatbot Service Implementation**:
    -   Create `chatbot_service.py` to house the agent orchestration logic.
    -   Initialize the OpenAI Agent with the defined task management tools.
    -   Implement methods to handle conversational turns, including:
        -   Retrieving/creating `ChatbotSession`.
        -   Adding user message to history.
        -   Invoking the OpenAI Agent with current conversation history.
        -   Processing agent's tool calls and responses.
        -   Updating conversation history with agent's response.
5.  **Chatbot API Endpoint**:
    -   Add `chatbot.py` under `backend/src/api`.
    -   Define a `POST /api/chatbot` endpoint that accepts a user message and returns the chatbot's response.
    -   Integrate with `auth_service` to ensure the user is authenticated and `user_id` is passed to the `chatbot_service`.

### Phase 2: Frontend Chat UI Integration

**Goal**: Provide a user-friendly interface for interacting with the chatbot.

1.  **Chat UI Component Development**:
    -   Create a new React component (`Chatbot.jsx`) for the chat interface.
    -   This component will include an input field for user messages, a display area for conversation history, and send/loading indicators.
2.  **Dashboard Integration**:
    -   Integrate the `Chatbot.jsx` component into the `Dashboard.jsx` or a new dedicated chat page in the Next.js frontend.
3.  **API Communication**:
    -   Implement client-side logic to send user messages to the `POST /api/chatbot` endpoint.
    -   Handle responses from the backend, updating the chat UI with chatbot messages.
    -   Manage loading states and error displays.

## 4. Risks & Mitigations

-   **Risk**: High latency from OpenAI API impacting user experience.
    -   **Mitigation**: Implement streaming responses if supported by OpenAI SDK and frontend. Display typing indicators. Optimize tool calls.
-   **Risk**: Agent "hallucinations" or incorrect tool usage.
    -   **Mitigation**: Strict tool definitions and robust input validation for tools. Implement clear error messages and fallback strategies.
-   **Risk**: Complex natural language queries leading to poor agent performance.
    -   **Mitigation**: Start with clear, simple prompts for tools. Gradually enhance agent's understanding through prompt engineering and potentially fine-tuning.

## 5. Open Questions & Research Areas

-   **Conversation State Management**: Detailed strategy for managing `conversation_history` in `ChatbotSession` (e.g., truncation, summarization for long conversations).
-   **Tool Definition Best Practices**: How to best define tools for the OpenAI Agents SDK to ensure robustness and minimize misinterpretations.
-   **Frontend Chat UI Libraries**: Evaluate existing React chat UI libraries for faster development (e.g., `react-chat-elements`, `react-chatbot-kit`).

## 6. Next Steps

-   Proceed to `/sp.tasks` to break down this plan into actionable tasks.