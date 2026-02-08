# Implementation Plan: Todo AI Chatbot

**Branch**: `001-ai-chatbot` | **Date**: 2026-02-06 | **Spec**: [specs/001-ai-chatbot/spec.md]
**Input**: Feature specification from `/specs/001-ai-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement an AI-powered chatbot that allows users to manage their todos using natural language commands. The solution will integrate with the existing todo application frontend and backend, utilizing MCP tools for secure task operations and the OpenAI Agents SDK for natural language processing. The system follows a stateless architecture with PostgreSQL as the single source of truth, ensuring real-time synchronization between chat and traditional UI interfaces.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.11, JavaScript/TypeScript (based on existing project)
**Primary Dependencies**: FastAPI, OpenAI Agents SDK, Better Auth, SQLModel, MCP SDK, React (for existing frontend)
**Storage**: PostgreSQL (Neon), with existing database schema for tasks, users, and conversations
**Testing**: pytest (backend), Jest/Cypress (frontend)
**Target Platform**: Web application (Linux server)
**Project Type**: Web (frontend + backend with existing components to integrate)
**Performance Goals**: <5s response time for chat interactions, support 100 concurrent users
**Constraints**: <200ms p95 latency for tool calls, stateless architecture per constitution, real-time sync between chat and UI
**Scale/Scope**: 1000 daily active users, integrate with existing todo app functionality

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Design Compliance Verification

**Core Principles**:
- ✅ Spec-driven development only: Following specification from spec.md
- ✅ No manual code writing: Will use automated tools for implementation
- ✅ Stateless server architecture: Chat API will maintain no session state between requests
- ✅ Database is the single source of truth: All data stored in PostgreSQL
- ✅ AI must act only through MCP tools: AI will interact via MCP tool calls only
- ✅ Tools must be deterministic and idempotent: MCP tools will be designed as such

**Architecture Rules**:
- ✅ FastAPI handles HTTP only: Chat endpoint will be HTTP-only
- ✅ OpenAI Agents SDK handles reasoning: AI reasoning through OpenAI Agents SDK
- ✅ MCP server exposes task operations as tools: All operations exposed as MCP tools
- ✅ MCP tools persist all state via SQLModel: State persistence through SQLModel
- ✅ No in-memory state anywhere: Stateless design enforced

**Behavior Rules**:
- ✅ Every user action maps to MCP tool calls: Natural language mapped to specific tools
- ✅ Agent confirms successful actions: AI will confirm all completed operations
- ✅ Errors handled gracefully: Error handling built into the system
- ✅ No hallucinated task data: AI will only operate on actual database data
- ✅ Tool usage logged: Tool calls will be logged and returned

**Security Rules**:
- ✅ Operations scoped by user_id: All operations will be user-scoped
- ✅ Authentication via Better Auth: Using existing Better Auth system
- ✅ No cross-user data leakage: Proper user isolation enforced

**Disallowed behaviors NOT present**:
- ✅ No hardcoded state
- ✅ No manual code edits (following automated approach)
- ✅ No business logic in frontend (keeping in backend)

### Post-Design Compliance Verification

After implementing the design:

**Core Principles** (all confirmed):
- ✅ Spec-driven development only: All design decisions trace back to spec requirements
- ✅ No manual code writing: Generated from contracts and data models
- ✅ Stateless server architecture: FastAPI endpoints maintain no session state
- ✅ Database is the single source of truth: All data stored in PostgreSQL via SQLModel
- ✅ AI must act only through MCP tools: All AI operations route through MCP tools
- ✅ Tools must be deterministic and idempotent: Designed with consistent behavior

**Architecture Rules** (all confirmed):
- ✅ FastAPI handles HTTP only: API endpoints handle only HTTP concerns
- ✅ OpenAI Agents SDK handles reasoning: AI reasoning encapsulated in agent module
- ✅ MCP server exposes task operations as tools: All operations available as MCP tools
- ✅ MCP tools persist all state via SQLModel: All persistence through SQLModel models
- ✅ No in-memory state anywhere: Stateless architecture confirmed

**Behavior Rules** (all confirmed):
- ✅ Every user action maps to MCP tool calls: Natural language mapped to specific tools
- ✅ Agent confirms successful actions: Responses include confirmation messages
- ✅ Errors handled gracefully: API contract includes error responses
- ✅ No hallucinated task data: AI operates only on actual database records
- ✅ Tool usage logged: Tool calls logged as part of API responses

**Security Rules** (all confirmed):
- ✅ Operations scoped by user_id: All endpoints verify user_id permissions
- ✅ Authentication via Better Auth: Authentication integrated into API
- ✅ No cross-user data leakage: Database queries include user_id filters

**Disallowed behaviors avoided**:
- ✅ No hardcoded state: All configuration externalized
- ✅ No manual code edits: Following automated generation approach
- ✅ No business logic in frontend: Business logic in backend services

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/                 # SQLModel database models (Task, Conversation, Message)
│   │   ├── task_model.py       # Task entity definition
│   │   ├── conversation_model.py # Conversation entity definition
│   │   └── message_model.py    # Message entity definition
│   ├── services/               # Business logic services
│   │   ├── task_service.py     # Task operations
│   │   ├── conversation_service.py # Conversation management
│   │   └── mcp_tool_service.py # MCP tool implementations
│   ├── api/                    # API endpoints
│   │   ├── chat_endpoint.py    # Main chat API endpoint
│   │   └── conversation_endpoint.py # Conversation management endpoints
│   ├── agents/                 # AI agent configuration
│   │   └── todo_agent.py       # Todo-specific AI agent
│   └── core/                   # Core utilities
│       ├── auth.py            # Better Auth integration
│       └── database.py        # Database connection setup
└── tests/
    ├── unit/
    ├── integration/
    └── contract/

frontend/
├── src/
│   ├── components/
│   │   ├── ChatWidget/        # Floating chat widget component
│   │   └── TodoChatView/      # Dedicated chat interface
│   ├── pages/
│   ├── services/
│   │   └── api.js            # API communication layer
│   └── hooks/
│       └── useChat.js        # Chat functionality hooks
└── tests/

mcp-server/
├── tools/                      # MCP tool definitions
│   ├── add_task.py
│   ├── list_tasks.py
│   ├── complete_task.py
│   ├── delete_task.py
│   └── update_task.py
└── src/                       # MCP server implementation
    └── server.py
```

**Structure Decision**: Selected Web application structure to integrate with existing frontend/backend architecture. Backend will implement the chat API and MCP tools, frontend will integrate the chat widget with existing UI components.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
