## FastAPI Post Service

A production-ready FastAPI application using SQLModel and PostgreSQL with JWT-based authentication, CRUD for posts, user management, and a simple voting system. Includes Alembic migrations and Pydantic v2 schemas.

### Features
- **Users**: create and fetch users
- **Auth**: OAuth2 password flow with JWT access tokens (`/login`)
- **Posts**: create, list (with vote counts), get, update, delete
- **Votes**: add/remove a vote to a post
- **DB**: PostgreSQL via SQLModel/SQLAlchemy
- **Migrations**: Alembic configured and ready
- **CORS**: permissive default (`*`) via middleware

### Tech Stack
- **API**: FastAPI, Starlette
- **Models/ORM**: SQLModel (SQLAlchemy + Pydantic models)
- **Auth**: `python-jose` (JWT), `passlib[bcrypt]`
- **DB**: PostgreSQL, `psycopg2`
- **Migrations**: Alembic

## Getting Started

### Prerequisites
- Python 3.12+
- PostgreSQL database

### Environment
Create a `.env` file in the project root with:

```env
# PostgreSQL
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=your_password
DATABASE_NAME=fastapiprac

# JWT
SECRET_KEY=your_super_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

The app reads these via `pydantic-settings` in `app/config.py` using the `.env` file.

### Installation
```bash
# (Recommended) create and activate a virtual environment
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirement.txt

# Ensure these are present (if missing in requirement.txt)
pip install sqlmodel python-jose[cryptography] passlib[bcrypt] psycopg2-binary
```

### Database Setup
You can initialize tables directly on app startup (the project calls `init_db()` which runs `SQLModel.metadata.create_all(engine)`). For production, prefer Alembic migrations.

#### Alembic Migrations
```bash
# Set env vars or .env as above so Alembic can build the URL
# Run existing migrations
alembic upgrade head

# Create a new migration after model changes
alembic revision -m "your message" --autogenerate
alembic upgrade head
```
Alembic is configured in `alembic/env.py` to use your `.env` values and `SQLModel.metadata`.

### Run the API
```bash
uvicorn app.main:app --reload
```
Server runs at `http://127.0.0.1:8000`. Interactive docs at `http://127.0.0.1:8000/docs`.

## API Overview

### Auth
- **POST** `/login`
  - Body (form): `username`, `password` (OAuth2PasswordRequestForm)
  - Returns: `{ "access_token": "...", "token_type": "bearer" }`
  - Use `Authorization: Bearer <access_token>` for protected routes

### Users
- **POST** `/users/`
  - Body: `{ "email": "user@example.com", "password": "secret" }`
  - Returns: user without password
- **GET** `/users/{id}`
  - Returns: user details

### Posts
- Requires Bearer token
- **GET** `/posts/`
  - Query: `limit` (default 10), `skip` (default 0), `search` (title contains)
  - Returns: list of `{ Post: <post>, votes: <int> }`
- **POST** `/posts/`
  - Body: `{ "title": "...", "content": "...", "published": true }`
  - Returns: created post
- **GET** `/posts/{id}`
  - Returns: `{ Post: <post>, votes: <int> }`
- **PUT** `/posts/{id}`
  - Body: same as POST body
  - Only owner can update
- **DELETE** `/posts/{id}`
  - Only owner can delete

### Votes
- Requires Bearer token
- **POST** `/vote/`
  - Body: `{ "post_id": 1, "dir": 1 }` where `dir=1` to add vote, `dir=0` to remove vote
  - Returns message on success

## Data Models (Simplified)
- `User`: `id`, `email`, `password`, `created_at`
- `Post`: `id`, `title`, `content`, `published`, `created_at`, `ownerid`, relationship `owner`
- `Vote`: composite PK of `user_id`, `post_id`

## Project Structure
```
app/
  main.py          # FastAPI app, CORS, router includes
  config.py        # pydantic BaseSettings (.env loader)
  database.py      # SQLModel engine, session, init_db
  model.py         # SQLModel tables: User, Post, Vote
  schemas.py       # Pydantic v2 schemas
  oauth2.py        # JWT creation/verification, get_current_user
  utils.py         # Password hashing/verification
  routers/
    auth.py        # /login
    user.py        # /users
    post.py        # /posts
    vote.py        # /vote
alembic/           # Alembic config and versions
```

## Notes
- CORS is currently set to `*`. Restrict `allow_origins` in `app/main.py` for production.
- `init_db()` auto-creates tables on startup. Consider disabling in production and relying solely on Alembic migrations.
- Ensure `requirement.txt` lists: `sqlmodel`, `python-jose[cryptography]`, `passlib[bcrypt]`, `psycopg2-binary`.

## License
MIT (or your preferred license).