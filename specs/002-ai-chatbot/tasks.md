# Tasks: AI-Powered Todo Chatbot

**Input**: Design documents from `/specs/002-ai-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Install OpenAI Agents SDK in `backend/requirements.txt` (Installed openai package in venv)
- [X] T002 [P] Configure environment variables for OpenAI API in `backend/.env`
- [X] T003 [P] Create `backend/src/chatbot` directory
- [X] T004 [P] Create `backend/src/api/chatbot.py`
- [X] T005 [P] Create `backend/src/services/chatbot_service.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [X] T006 Define `ChatbotSession` SQLModel in `backend/src/models/chatbot.py`
- [X] T007 [P] Define `ToolCallLog` SQLModel in `backend/src/models/chatbot.py`
- [ ] T008 Run Alembic migrations to update the database schema (NEEDS TO BE RUN MANUALLY: `docker-compose up -d db` and then `source backend/venv/bin/activate && cd backend && alembic upgrade head`)
- [X] T009 Create task management tools in `backend/src/services/chatbot_service.py` (wrapping `task_service` functions)

---

## Phase 3: User Story 1 - Create a new task (Priority: P1) 🎯 MVP

**Goal**: Allow users to create a new task via chatbot.

**Independent Test**: Type "add a new task to buy milk" and verify the task is created in the database.

### Implementation for User Story 1

- [X] T010 [US1] Implement `create_task_tool` in `backend/src/services/chatbot_service.py`
- [X] T011 [US1] Implement conversation logic for creating tasks in `backend/src/services/chatbot_service.py`
- [X] T012 [US1] Implement the `POST /api/chatbot` endpoint in `backend/src/api/chatbot.py` to handle task creation
- [X] T013 [P] [US1] Create a basic chat UI component `frontend/src/components/Chatbot.jsx`
- [X] T014 [US1] Integrate the chat UI with the dashboard in `frontend/src/components/Dashboard.jsx`
- [X] T015 [US1] Connect the chat UI to the backend API for creating tasks in `frontend/src/components/Chatbot.jsx`

---

## Phase 4: User Story 2 - Read all tasks (Priority: P1)

**Goal**: Allow users to read all their tasks via chatbot.

**Independent Test**: Type "show me all my tasks" and verify the chatbot returns a list of all tasks.

### Implementation for User Story 2

- [ ] T016 [US2] Implement `get_tasks_tool` in `backend/src/services/chatbot_service.py`
- [ ] T017 [US2] Implement conversation logic for reading tasks in `backend/src/services/chatbot_service.py`
- [ ] T018 [US2] Update the `POST /api/chatbot` endpoint in `backend/src/api/chatbot.py` to handle reading tasks
- [ ] T019 [US2] Update the chat UI to display the list of tasks in `frontend/src/components/Chatbot.jsx`

---

## Phase 5: User Story 3 - Update a task (Priority: P2)

**Goal**: Allow users to update a task via chatbot.

**Independent Test**: Type "update task 1 to 'buy almond milk'" and verify the task is updated in the database.

### Implementation for User Story 3

- [ ] T020 [US3] Implement `update_task_tool` in `backend/src/services/chatbot_service.py`
- [ ] T021 [US3] Implement conversation logic for updating tasks in `backend/src/services/chatbot_service.py`
- [ ] T022 [US3] Update the `POST /api/chatbot` endpoint in `backend/src/api/chatbot.py` to handle updating tasks
- [ ] T023 [US3] Update the chat UI to reflect the updated task in `frontend/src/components/Chatbot.jsx`

---

## Phase 6: User Story 4 - Delete a task (Priority: P2)

**Goal**: Allow users to delete a task via chatbot.

**Independent Test**: Type "delete task 1" and verify the task is deleted from the database.

### Implementation for User Story 4

- [ ] T024 [US4] Implement `delete_task_tool` in `backend/src/services/chatbot_service.py`
- [ ] T025 [US4] Implement conversation logic for deleting tasks in `backend/src/services/chatbot_service.py`
- [ ] T026 [US4] Update the `POST /api/chatbot` endpoint in `backend/src/api/chatbot.py` to handle deleting tasks
- [ ] T027 [US4] Update the chat UI to remove the deleted task in `frontend/src/components/Chatbot.jsx`

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T028 [P] Implement summarization strategy for conversation history in `backend/src/services/chatbot_service.py`
- [ ] T029 [P] Implement tool usage logging in `backend/src/services/chatbot_service.py`
- [ ] T030 [P] Implement error handling for unknown/ambiguous commands in `backend/src/services/chatbot_service.py`
- [ ] T031 [P] Add documentation for the chatbot API.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed sequentially in priority order (P1 → P2).

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2)
- **User Story 2 (P1)**: Can start after Foundational (Phase 2)
- **User Story 3 (P2)**: Can start after Foundational (Phase 2)
- **User Story 4 (P2)**: Can start after Foundational (Phase 2)

### Within Each User Story

- Backend tasks before frontend tasks.

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- Foundational tasks T006 and T007 can run in parallel
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Polish tasks marked [P] can run in parallel

---

## Implementation Strategy

### MVP First (User Story 1 & 2)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3 & 4: User Story 1 & 2
4. **STOP and VALIDATE**: Test User Story 1 & 2 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 & 2 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 3 & 4 → Test independently → Deploy/Demo
