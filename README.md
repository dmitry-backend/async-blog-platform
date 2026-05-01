# AsyncBlog Platform
A modern real-world async full-stack blogging platform built with FastAPI, React, PostgreSQL, Celery and Redis. The project demonstrates a production-style architecture including authentication, database management, caching, and background task processing.

![App Screenshot](./screenshot.jpg)

## Features
- User registration and login (JWT authentication)
- Create blog posts
- Pagination on the home page
- Protected routes (only authenticated users can create posts)
- Redis caching for improved performance
- Background tasks using Celery
- Responsive user interface

## Tech Stack

### Backend
- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy (async)
- Alembic (database migrations)
- Redis
- Celery
- JWT authentication (python-jose)
- Password hashing (Argon2)

### Frontend
- React 19
- Vite
- React Router
- Context API (authentication)
- Fetch API

## Project Structure
```
async-blog-platform/
├── backend/
│   ├── app/
│   ├── alembic/
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
├── .gitignore
├── README.md
├── screenshot.jpg
└── LICENSE
```

## Getting Started

### Prerequisites
- Python 3.12+
- Node.js 18+
- PostgreSQL
- Redis

## Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables
Copy the example environment file:

```bash
# Linux / Mac
cp .env.example .env

# Windows
copy .env.example .env
```

Update values if needed.

Example `.env.example`:

```
DATABASE_URL=postgresql+asyncpg://user:password@localhost/db_name
REDIS_URL=redis://localhost:6379
SECRET_KEY=your_secret_key
```

### Run Database Migrations
```bash
alembic upgrade head
```

### Start Backend Server
```bash
uvicorn app.main:app --reload --port 8000
```

Backend: http://localhost:8000

## Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Environment Variables
Copy the example environment file:

```bash
# Linux / Mac
cp .env.example .env

# Windows
copy .env.example .env
```

Example `.env.example`:
```
VITE_API_URL=http://localhost:8000
```

Frontend: http://localhost:5173

## API Overview

### Authentication
- `POST /auth/register` — Register a new user
- `POST /auth/login` — Authenticate user and return JWT

### Posts
- `GET /posts` — Get paginated list of posts
- `GET /posts/{id}` — Get a single post
- `POST /posts` — Create post (auth required)
- `PUT /posts/{id}` — Update post (auth required)
- `DELETE /posts/{id}` — Delete post (auth required)

## Background Tasks
Celery is used for asynchronous task processing.

Run worker:
```bash
celery -A app.worker worker --loglevel=info
```

Make sure Redis is running before starting the worker.

## Caching
Redis is used to cache frequently requested data (e.g., post lists) to reduce database load and improve response times.

## License
This project is licensed under the MIT License.
