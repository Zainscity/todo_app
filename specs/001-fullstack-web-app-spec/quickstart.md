# Quick Start Guide

## Prerequisites

- Node.js 18+ for frontend development
- Python 3.13+ for backend development
- PostgreSQL-compatible database (Neon Serverless recommended)
- `uv` package manager for Python dependencies

## Environment Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd hackathon-todo
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Install Python dependencies using uv
uv pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database connection string and auth secrets
```

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install JavaScript dependencies
npm install
# or
yarn install

# Set up environment variables
cp .env.local.example .env.local
# Edit .env.local with your API endpoints and auth configuration
```

## Running the Application

### 1. Start the Backend
```bash
cd backend
uv run python -m src.main
# or with uvicorn directly
uvicorn src.main:app --reload --port 8000
```

### 2. Start the Frontend
```bash
cd frontend
npm run dev
# or
yarn dev
```

### 3. Access the Application
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- Backend docs: `http://localhost:8000/docs`

## Development Commands

### Backend Commands
```bash
# Run tests
pytest

# Run with auto-reload during development
uvicorn src.main:app --reload

# Format code
black src/
```

### Frontend Commands
```bash
# Development server
npm run dev

# Build for production
npm run build

# Run tests
npm run test

# Lint code
npm run lint
```

## Database Setup

### 1. Initialize Database
```bash
# With the backend running
curl -X POST http://localhost:8000/api/init-db
```

### 2. Environment Variables
Set the following in your `.env` file:
```env
DATABASE_URL="postgresql://username:password@host:port/database_name"
SECRET_KEY="your-secret-key-for-jwt-signing"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## API Usage

### Authentication
All API endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt-token>
```

### Example API Call
```bash
curl -X GET \
  http://localhost:8000/api/user-id/tasks \
  -H "Authorization: Bearer your-jwt-token" \
  -H "Content-Type: application/json"
```

## Troubleshooting

### Common Issues
1. **Port Already in Use**: Change the port in the configuration files
2. **Database Connection**: Verify DATABASE_URL is correctly set
3. **Authentication Errors**: Ensure JWT tokens are valid and properly formatted
4. **Frontend Cannot Connect to Backend**: Check that CORS is configured correctly

### Useful Commands
```bash
# Check backend health
curl http://localhost:8000/health

# View API documentation
open http://localhost:8000/docs
```