---
id: 1
title: Amend Todo App Constitution
stage: constitution
date: 2026-02-05
surface: agent
model: claude-haiku-4-5-20251001
feature: none
branch: 001-fullstack-web-app-spec
user: default_user
command: /sp.constitution
labels: [constitution, todo-app, ai-chatbot, spec-driven-development]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

/sp.constitution

You are building Phase III of a Todo application: an AI-powered chatbot.

Core Principles:
- Spec-driven development only
- No manual code writing
- Stateless server architecture
- Database is the single source of truth
- AI must act only through MCP tools
- Tools must be deterministic and idempotent

Architecture Rules:
- FastAPI handles HTTP only
- OpenAI Agents SDK handles reasoning
- MCP server exposes task operations as tools
- MCP tools persist all state via SQLModel
- No in-memory state anywhere

Behavior Rules:
- Every user action must map to exactly one or more MCP tool calls
- Agent must confirm all successful actions
- Errors must be handled gracefully and explained
- No hallucinated task data
- Tool usage must be logged and returned in response

Security Rules:
- All operations are scoped by user_id
- Authentication handled via Better Auth
- No cross-user data leakage

Judging Criteria:
- Correct use of MCP
- Correct use of OpenAI Agents SDK
- Clean stateless request cycle
- Accurate natural language → tool mapping
- Clear separation of concerns

Disallowed:
- Hardcoded state
- Manual code edits
- Skipping Spec-Kit steps
- Business logic inside frontend

Always prioritize correctness, clarity, and auditability.

## Response snapshot

Updated the project constitution at .specify/memory/constitution.md with the specified principles and rules for the AI-powered chatbot Todo application. The constitution now includes:

- Core Principles: Spec-driven development only, No manual code writing, Stateless server architecture, Database is the single source of truth, AI must act only through MCP tools, Tools must be deterministic and idempotent
- Architecture Rules: FastAPI for HTTP, OpenAI Agents SDK for reasoning, MCP tools for operations, SQLModel for persistence, stateless architecture
- Behavior Rules: MCP tool mappings, action confirmations, error handling, no hallucinated data, tool usage logging
- Security Rules: User scoping, Better Auth authentication, data isolation
- Judging Criteria: MCP usage, OpenAI SDK usage, stateless cycles, NL-to-tool mapping, separation of concerns
- Disallowed items: Hardcoded state, manual edits, skipped steps, frontend business logic

## Outcome

- ✅ Impact: Updated constitution with all required principles for AI-powered Todo app
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md
- 🔁 Next prompts: Continue with spec-driven development for the AI chatbot
- 🧠 Reflection: Constitution now properly defines the development approach and constraints for the project

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS - All principles properly incorporated
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): Begin specification development based on the new constitution