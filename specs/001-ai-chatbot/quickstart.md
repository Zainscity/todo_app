# Quickstart Guide: Todo AI Chatbot

## Overview
This guide explains how to set up and start developing the AI-powered chatbot for the todo application.

## Prerequisites
- Python 3.11+
- Node.js 18+ (for existing frontend)
- PostgreSQL (or NeonDB connection)
- Poetry (for Python dependency management)
- Git

## Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd todo_app
git checkout 001-ai-chatbot  # Switch to feature branch
```

### 2. Backend Setup
```bash
cd backend
poetry install  # Install Python dependencies
poetry shell  # Activate virtual environment

# Set up environment variables
cp .env.example .env
# Edit .env with your database URL, Better Auth keys, etc.

# Run database migrations
python -m src.core.database migrate

# Start the backend server
poetry run uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. MCP Server Setup
```bash
cd mcp-server
poetry install
poetry shell

# Start the MCP server
poetry run python src/server.py
```

### 4. Frontend Setup
```bash
cd frontend  # or main directory if frontend is co-located
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with API endpoints, auth config, etc.

# Start the frontend
npm start
```

## Key Components

### Backend Structure
```
backend/
├── src/
│   ├── models/                 # SQLModel definitions
│   ├── services/               # Business logic
│   ├── api/                    # FastAPI endpoints
│   ├── agents/                 # AI agent configuration
│   └── core/                   # Core utilities
└── tests/
```

### Key Endpoints
- `POST /api/{user_id}/chat` - Main chat endpoint
- `GET /api/{user_id}/conversations` - List conversations
- `GET /api/{user_id}/conversations/{id}` - Get conversation details

### MCP Tools
The system includes these MCP tools for AI operations:
- `add_task` - Add a new task
- `list_tasks` - List user's tasks
- `complete_task` - Mark a task as complete
- `delete_task` - Remove a task
- `update_task` - Modify task details

## Development Commands

### Backend Development
```bash
# Run tests
poetry run pytest

# Format code
poetry run black src/
poetry run ruff check src/

# Run backend with auto-reload
poetry run uvicorn src.api.main:app --reload
```

### Running the Full System
```bash
# Terminal 1: Start database (if using local)
docker-compose up postgres

# Terminal 2: Start MCP server
cd mcp-server && poetry run python src/server.py

# Terminal 3: Start backend
cd backend && poetry run uvicorn src.api.main:app --reload

# Terminal 4: Start frontend
cd frontend && npm start
```

## Integration Points

### Chat Widget
The chat widget is designed to be embedded in existing pages. Add this to any page:
```jsx
import { ChatWidget } from './components/ChatWidget';

function MyPage() {
  return (
    <div>
      <h1>My Page</h1>
      {/* Existing content */}
      <ChatWidget />
    </div>
  );
}
```

### Data Consistency
All operations through the chatbot update the same underlying data as the traditional UI, ensuring real-time synchronization.

## Troubleshooting

### Common Issues
1. **Authentication Errors**: Verify Better Auth is configured correctly in both frontend and backend
2. **MCP Connection Issues**: Check that MCP server is running and properly configured
3. **Database Connectivity**: Confirm DATABASE_URL is set correctly in environment variables

### Debugging the Chat Flow
1. Enable debug logging in the backend
2. Check the network tab in browser dev tools for API calls
3. Monitor MCP tool executions in server logs