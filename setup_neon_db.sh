#!/bin/bash

# Neon Database Setup Script for Todo App

echo "========================================="
echo "Todo App - Neon Database Setup"
echo "========================================="

# Check if psql is installed
if ! command -v psql &> /dev/null; then
    echo "❌ psql is not installed. Please install PostgreSQL client tools."
    echo "   On Ubuntu/Debian: sudo apt-get install postgresql-client"
    echo "   On macOS: brew install libpq"
    exit 1
fi

echo ""
echo "📝 Before proceeding, ensure you have:"
echo "   1. Created a Neon account at https://neon.tech"
echo "   2. Created a project in Neon Dashboard"
echo "   3. Copied your connection string from Project Settings"
echo ""

read -p "Enter your Neon connection string (format: postgresql://user:pass@ep-xxx.region.aws.neon.tech/dbname): " CONNECTION_STRING

if [[ -z "$CONNECTION_STRING" ]]; then
    echo "❌ No connection string provided. Exiting."
    exit 1
fi

echo ""
echo "🔧 Setting up environment variables..."

# Extract database name from connection string
DB_NAME=$(echo "$CONNECTION_STRING" | sed -n 's/.*\/\([^?]*\).*/\1/p')

if [[ -z "$DB_NAME" ]]; then
    echo "❌ Could not extract database name from connection string."
    exit 1
fi

echo ""
echo "Database name detected: $DB_NAME"

# Create backend .env file
cat > /mnt/c/Files/code/Quarter 4/Hackathon_2/todo_app/backend/.env << EOF
# Database
DATABASE_URL=$CONNECTION_STRING

# Auth
SECRET_KEY=$(openssl rand -hex 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server
HOST=0.0.0.0
PORT=8000
APP_NAME=Todo App Backend
VERSION=1.0.0

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:3001"]
EOF

echo "✅ Backend .env file created"

# Create frontend .env.local file
cat > /mnt/c/Files/code/Quarter 4/Hackathon_2/todo_app/frontend/.env.local << EOF
# API
NEXT_PUBLIC_API_URL=http://localhost:8000/api

# Auth
NEXT_PUBLIC_JWT_SECRET=$(openssl rand -hex 16)
EOF

echo "✅ Frontend .env.local file created"

echo ""
echo "🎉 Neon database setup complete!"
echo ""
echo "📁 Files created:"
echo "   - backend/.env (with your Neon connection string)"
echo "   - frontend/.env.local (with API configuration)"
echo ""
echo "🚀 To run locally:"
echo "   1. cd backend && pip install -r requirements.txt"
echo "   2. cd backend && uvicorn src.main:app --reload"
echo "   3. In another terminal: cd frontend && npm install && npm run dev"
echo ""
echo "🌐 For Vercel deployment, push your code and set environment variables in the Vercel dashboard"
echo ""
echo "💡 Remember to update NEXT_PUBLIC_API_URL in frontend/.env.local when deploying to production"