# Data Model: Todo AI Chatbot

## Overview

This document defines the database schema for the Todo AI Chatbot feature, extending the existing todo application data model to support conversational interfaces while maintaining consistency with existing functionality.

## Entity Definitions

### Task Entity
**Table**: `tasks`
**Description**: Represents a user's todo item with properties for management via both UI and chat interface

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | Primary Key, Auto-increment | Unique identifier for the task |
| user_id | String | Not Null, Foreign Key | Identifier of the user who owns this task |
| title | String(255) | Not Null | Brief title/description of the task |
| description | Text | Nullable | Detailed description of the task |
| completed | Boolean | Not Null, Default: False | Whether the task has been completed |
| created_at | DateTime | Not Null | Timestamp when task was created |
| updated_at | DateTime | Not Null | Timestamp when task was last updated |

**Validation Rules**:
- Title must not be empty
- user_id must reference a valid user
- created_at and updated_at must be in UTC

**State Transitions**:
- Active → Completed (when task is marked as done)
- Completed → Active (when task is unmarked)

### Conversation Entity
**Table**: `conversations`
**Description**: Represents a thread of communication between a user and the AI assistant

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | Primary Key, Auto-increment | Unique identifier for the conversation |
| user_id | String | Not Null, Foreign Key | Identifier of the user participating in this conversation |
| created_at | DateTime | Not Null | Timestamp when conversation started |
| updated_at | DateTime | Not Null | Timestamp when conversation was last updated |

**Validation Rules**:
- user_id must reference a valid user
- created_at and updated_at must be in UTC

### Message Entity
**Table**: `messages`
**Description**: Represents a single exchange in a conversation, either from the user or the assistant

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | Primary Key, Auto-increment | Unique identifier for the message |
| user_id | String | Not Null, Foreign Key | Identifier of the user who sent this message |
| conversation_id | Integer | Not Null, Foreign Key | Reference to the conversation this message belongs to |
| role | String | Not Null, Enum('user', 'assistant') | Who sent this message (user or AI assistant) |
| content | Text | Not Null | The actual content of the message |
| created_at | DateTime | Not Null | Timestamp when message was created |

**Validation Rules**:
- user_id must reference a valid user
- conversation_id must reference a valid conversation
- role must be either 'user' or 'assistant'
- content must not be empty
- created_at must be in UTC

## Relationships

### Task ↔ User
- **Relationship**: Many-to-One (Many tasks belong to one user)
- **Constraint**: Cascading delete not allowed (tasks are critical data)

### Conversation ↔ User
- **Relationship**: Many-to-One (Many conversations belong to one user)
- **Constraint**: Cascading delete allowed (conversation history can be deleted when user is removed)

### Message ↔ User
- **Relationship**: Many-to-One (Many messages belong to one user)
- **Constraint**: Cascading delete allowed (messages can be deleted when user is removed)

### Message ↔ Conversation
- **Relationship**: Many-to-One (Many messages belong to one conversation)
- **Constraint**: Cascading delete (messages deleted when conversation is deleted)

## Indexes

### Required Indexes:
- `tasks.user_id_idx`: Index on user_id for efficient user-specific queries
- `conversations.user_id_idx`: Index on user_id for efficient user-specific queries
- `messages.conversation_id_idx`: Index on conversation_id for efficient conversation retrieval
- `messages.user_id_idx`: Index on user_id for efficient user-specific queries
- `tasks.completed_idx`: Index on completed status for filtering completed/incomplete tasks

### Composite Indexes:
- `messages.conversation_created_idx`: Composite index on (conversation_id, created_at) for chronological message retrieval
- `tasks.user_completed_idx`: Composite index on (user_id, completed) for efficient user task queries

## Database Constraints

### Referential Integrity:
- All foreign key relationships enforce referential integrity
- Orphaned records are prevented through foreign key constraints

### Data Validation:
- Non-null constraints on required fields
- Enum constraints on role field in messages table
- Length constraints on text fields to prevent oversized data

## API Contract Implications

The data model supports:
- Real-time synchronization between chat and UI (via consistent task records)
- Conversation history preservation
- User isolation through user_id scoping
- Efficient querying for task lists and conversation threads
- Audit trail through creation and update timestamps