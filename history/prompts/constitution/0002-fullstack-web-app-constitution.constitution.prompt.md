---
id: 0002
title: Fullstack Web App Constitution
stage: constitution
date: 2026-01-30
surface: agent
model: claude-haiku-4-5-20251001
feature: none
branch: master
user: default_user
command: sp.constitution
labels: [constitution,fullstack,webapp,todo]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
---

## Prompt

```text
You are acting as a senior full-stack engineer operating under strict spec-driven
development using Spec-Kit Plus and Claude Code.

Project Name:
Todo Full-Stack Web Application (Phase II – Web + Multi-User)

Phase Context:
(MANDATORY SKILL USAGE:
You MUST use the Claude skill `skill/fullstack_setup`
for this phase.)
This phase is a continuation of Phase I (Console Todo App).
All Phase I task behavior (CRUD + completion) MUST be preserved,
but the implementation is transformed into a full-stack web application
with persistent storage and authentication.

Primary Objective:
Transform the existing in-memory console Todo application into a modern,
secure, multi-user web application with:
- RESTful API
- Persistent database storage
- Authentication
- Responsive frontend UI

Scope (Phase II Only):
- Web-based application (no console UI)
- Multi-user support
- Persistent storage using PostgreSQL
- Authenticated access to all task data
- Monorepo structure supporting frontend and backend in a single repository

Core Functional Requirements:
The system MUST implement all five core task features as a web application:

1. Create Task
2. View/List Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete / Incomplete

Each task MUST:
- Belong to a specific authenticated user
- Be inaccessible to other users
- Persist across application restarts

Authentication Requirements:
- Implement user signup and signin using Better Auth
- Use JWT-based authentication
- Secure all task-related API endpoints
- Users may only access their own tasks

API Requirements:
- Backend must expose RESTful endpoints via FastAPI
- All endpoints must be prefixed with `/api/`
- Endpoints must follow this contract:

  GET    /api/{user_id}/tasks
  POST   /api/{user_id}/tasks
  GET    /api/{user_id}/tasks/{id}
  PUT    /api/{user_id}/tasks/{id}
  DELETE /api/{user_id}/tasks/{id}
  PATCH  /api/{user_id}/tasks/{id}/complete

- All endpoints require valid authentication
- Responses must be JSON
- Errors must return proper HTTP status codes

Frontend Requirements:
- Built with Next.js 16+ using App Router
- Responsive UI
- Communicates with backend exclusively via REST API
- Uses a centralized API client abstraction
- Displays task status clearly (completed vs pending)

Backend Requirements:
- Built with Python FastAPI
- Use SQLModel as ORM
- Use Neon Serverless PostgreSQL for persistence
- Database connection via environment variable
- No raw SQL unless explicitly specified

Database Requirements:
- Users table managed by Better Auth
- Tasks table must include:
  - id
  - user_id (foreign key)
  - title
  - description
  - completed
  - created_at
  - updated_at

Repository Organization (Mandatory):
This project MUST be organized as a monorepo:

hackathon-todo/
├── .spec-kit/
│   └── config.yaml
├── specs/
│   ├── overview.md
│   ├── architecture.md
│   ├── features/
│   │   ├── task-crud.md
│   │   └── authentication.md
│   ├── api/
│   │   └── rest-endpoints.md
│   ├── database/
│   │   └── schema.md
│   └── ui/
│       ├── components.md
│       └── pages.md
├── frontend/
│   ├── CLAUDE.md
│   └── (Next.js app)
├── backend/
│   ├── CLAUDE.md
│   └── (FastAPI app)
├── CLAUDE.md
├── docker-compose.yml
└── README.md

Spec-Driven Rules (Strict):
- No code may be written without an approved spec
- All behavior must be traceable to a spec file
- Specs must be updated before changing behavior
- Do NOT implement features outside Phase II scope
- Console-based features from Phase I must NOT reappear

Development Workflow:
1. Read or generate specs in `/specs`
2. Implement backend changes per specs
3. Implement frontend changes per specs
4. Validate feature behavior against acceptance criteria

Non-Goals (Explicitly Excluded):
- Chatbot features
- File-based storage
- Admin roles
- Task sharing between users
- Real-time updates (WebSockets)

Success Criteria:
- Authenticated users can fully manage their own tasks
- Data persists in Neon PostgreSQL
- API is secured and spec-compliant
- Frontend and backend coexist cleanly in monorepo
- Claude Code can navigate and modify both layers using specs
```

## Response snapshot

Updated the project constitution to reflect the transition from a console-based todo app to a full-stack web application with multi-user support, authentication, and persistent storage. The new constitution includes principles for clean architecture, persistent database storage, multi-user authentication and authorization, error handling, RESTful API design, and modern web technology stack. It also defines constraints for the technology stack, API requirements, database requirements, frontend requirements, data model requirements, and code quality standards. The repository organization follows a monorepo structure with separate frontend and backend directories.

## Outcome

- ✅ Impact: Updated constitution to reflect Phase II requirements (full-stack web app with auth)
- 🧪 Tests: No tests run for constitution update
- 📁 Files: 1 file updated (.specify/memory/constitution.md)
- 🔁 Next prompts: Implement backend API and authentication
- 🧠 Reflection: Constitution properly updated to guide full-stack development

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementing backend API endpoints