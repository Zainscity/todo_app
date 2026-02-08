# Todo Full-Stack Web Application (Phase II)

A modern, secure, multi-user todo application with persistent storage and authentication.

## Features

- User registration and authentication
- Create, read, update, delete, and mark tasks complete/incomplete
- Multi-user support with individual task ownership
- Persistent storage using PostgreSQL
- Responsive web interface

## Tech Stack

- **Frontend**: Next.js 16+ with App Router
- **Backend**: Python FastAPI
- **Database**: PostgreSQL (Neon Serverless)
- **Authentication**: Better Auth with JWT tokens
- **ORM**: SQLModel

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.13+
- PostgreSQL-compatible database
- `uv` package manager (optional but recommended)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd todo-fullstack-app
   ```

2. Set up the backend:
   ```bash
   cd backend
   pip install -r requirements.txt
   # Or with uv:
   uv pip install -r requirements.txt
   ```

3. Set up the frontend:
   ```bash
   cd frontend
   npm install
   # Or with yarn:
   yarn install
   ```

4. Set up environment variables:
   ```bash
   # In backend directory
   cp .env.example .env
   # Edit .env with your database connection string and auth secrets

   # In frontend directory
   cp .env.local.example .env.local
   # Edit .env.local with your API endpoints and auth configuration
   ```

### Running the Application

1. Start the backend:
   ```bash
   cd backend
   uvicorn src.main:app --reload --port 8000
   ```

2. Start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```

3. Access the application:
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:8000`
   - Backend docs: `http://localhost:8000/docs`

## Project Structure

```
hackathon-todo/
├── specs/                 # Feature specifications
├── frontend/              # Next.js frontend application
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── utils/
│   ├── package.json
│   └── README.md
├── backend/               # FastAPI backend application
│   ├── src/
│   │   ├── models/
│   │   ├── services/
│   │   ├── api/
│   │   └── auth/
│   ├── requirements.txt
│   └── README.md
├── docker-compose.yml     # Docker configuration for local development
└── README.md              # This file
```

## API Endpoints

All API endpoints are prefixed with `/api/`:

- `GET    /api/{user_id}/tasks` - Get all tasks for a user
- `POST   /api/{user_id}/tasks` - Create a new task for a user
- `GET    /api/{user_id}/tasks/{id}` - Get a specific task
- `PUT    /api/{user_id}/tasks/{id}` - Update a task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task
- `PATCH  /api/{user_id}/tasks/{id}/complete` - Toggle task completion status

All endpoints require valid JWT authentication.

## Deployment

For detailed deployment instructions to Vercel with Neon database, see [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md).

### Quick Deployment Steps

1. **Deploy Backend to Vercel**:
   ```bash
   cd backend
   vercel --prod
   ```

2. **Deploy Frontend to Vercel**:
   ```bash
   cd frontend
   vercel --prod
   ```

3. **Configure Environment Variables**:
   - Add your Neon database connection string
   - Set JWT secret and other required variables
   - Update frontend API URL to point to deployed backend

For complete deployment instructions including environment variable setup, see the [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) file.