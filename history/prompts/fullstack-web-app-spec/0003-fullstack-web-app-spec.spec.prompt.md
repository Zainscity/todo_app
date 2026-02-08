---
id: 0003
title: Fullstack Web App Spec
stage: spec
date: 2026-01-30
surface: agent
model: claude-haiku-4-5-20251001
feature: fullstack-web-app-spec
branch: 001-fullstack-web-app-spec
user: default_user
command: sp.specify
labels: [spec,fullstack,webapp,todo]
links:
  spec: specs/001-fullstack-web-app-spec/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-fullstack-web-app-spec/spec.md
 - specs/001-fullstack-web-app-spec/overview.md
 - specs/001-fullstack-web-app-spec/architecture.md
 - specs/001-fullstack-web-app-spec/features/task-crud.md
 - specs/001-fullstack-web-app-spec/features/authentication.md
 - specs/001-fullstack-web-app-spec/api/rest-endpoints.md
 - specs/001-fullstack-web-app-spec/database/schema.md
 - specs/001-fullstack-web-app-spec/ui/components.md
 - specs/001-fullstack-web-app-spec/ui/pages.md
 - specs/001-fullstack-web-app-spec/checklists/requirements.md
tests:
---

## Prompt

```text
You are operating under the Phase II constitution for the
Todo Full-Stack Web Application.

MANDATORY:
Use the Claude skill `skill/fullstack_setup` when reasoning about
architecture, frontend–backend interaction, database design,
authentication flow, and monorepo organization.

Objective:
Generate the complete Phase II specifications required to implement
the full-stack web version of the Todo application.

Specification Scope:
Create or update the following specifications inside the /specs directory:

1. overview.md
   - Phase II goals and scope
   - Differences from Phase I
   - Supported features and exclusions

2. architecture.md
   - High-level system architecture
   - Frontend (Next.js) ↔ Backend (FastAPI) interaction
   - Authentication flow using Better Auth
   - Database access via SQLModel + Neon PostgreSQL

3. features/task-crud.md
   - User stories for all five task operations
   - Acceptance criteria for each operation
   - User isolation rules (tasks per user only)
   - Validation rules (title length, description limits, etc.)

4. features/authentication.md
   - Signup and signin flows
   - JWT issuance and validation
   - Protected routes and authorization rules
   - Error cases (invalid token, expired token, unauthorized access)

5. api/rest-endpoints.md
   - REST API contract for all endpoints
   - HTTP methods, paths, request/response schemas
   - Authentication requirements per endpoint
   - Error responses and status codes

6. database/schema.md
   - SQLModel-based schema definition
   - Users table (managed by Better Auth)
   - Tasks table with relations and constraints
   - Indexing and data integrity rules

7. ui/components.md
   - Core UI components (TaskList, TaskItem, AuthForm, etc.)
   - Component responsibilities and data flow

8. ui/pages.md
   - App Router page structure
   - Protected vs public pages
   - Navigation flow after login/logout

Specification Rules:
- Do NOT write any code
- Each spec must be self-contained and unambiguous
- Specs must align with the Phase II constitution
- Specs must be suitable for direct implementation by Claude Code
- Avoid referencing implementation details not covered by specs

Constraints:
- Multi-user only (no shared tasks)
- Persistent storage required
- All task access must be authenticated
- Console UI is explicitly excluded

Output Requirements:
- Generate clean, markdown-based specification documents
- Follow the monorepo structure defined in the constitution
- Use clear headings and acceptance criteria
- No code blocks unless describing schemas or API payloads

Stop after generating specifications.
Do not proceed to implementation.
```

## Response snapshot

Generated complete Phase II specifications for the Todo Full-Stack Web Application, including all required documents: overview, architecture, task CRUD operations, authentication, API endpoints, database schema, UI components, and UI pages. Each specification document is self-contained, follows the constitution requirements, and provides clear acceptance criteria and technical specifications without implementation details. All specifications align with the Phase II constitution for the multi-user web application with authentication and persistent storage.

## Outcome

- ✅ Impact: Complete specification suite created for full-stack todo app
- 🧪 Tests: No tests run for specification creation
- 📁 Files: 10 files created across the spec directory structure
- 🔁 Next prompts: Ready for planning phase (/sp.plan)
- 🧠 Reflection: All required specifications completed according to constitution

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to planning phase