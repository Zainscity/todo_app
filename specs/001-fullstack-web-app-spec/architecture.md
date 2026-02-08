# System Architecture

## High-Level Architecture

The Todo application follows a clean architecture pattern with clear separation between frontend and backend layers:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Database      │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│  (PostgreSQL)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Browser       │    │   Authentication│    │   Neon          │
│   Client        │    │   (Better Auth) │    │   Serverless    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Frontend (Next.js) ↔ Backend (FastAPI) Interaction

The frontend communicates with the backend exclusively through REST API endpoints. Communication patterns include:

- **HTTP Requests**: All data exchange occurs via standard HTTP methods (GET, POST, PUT, DELETE, PATCH)
- **JSON Payloads**: Request and response bodies use JSON format for data serialization
- **API Prefix**: All endpoints are prefixed with `/api/` as per specification
- **Client-Side Rendering**: Next.js app router handles navigation and state management

## Authentication Flow using Better Auth

The authentication system implements JWT-based security with the following flow:

1. **Registration**: User submits credentials to `/api/auth/register` endpoint
2. **Login**: User credentials verified, JWT token issued and stored in browser
3. **Token Validation**: All subsequent API requests include Authorization header with JWT
4. **Session Management**: Tokens are refreshed automatically before expiration
5. **Logout**: JWT token invalidated and cleared from browser storage

## Database Access via SQLModel + Neon PostgreSQL

Database interactions follow these patterns:

- **ORM Layer**: SQLModel provides object-relational mapping for type-safe database operations
- **Connection Pooling**: Neon Serverless PostgreSQL manages connections efficiently
- **Environment Configuration**: Database connection string provided via environment variables
- **Transaction Safety**: All database operations use proper transaction handling
- **Data Integrity**: Foreign key constraints and validation rules enforced at database level