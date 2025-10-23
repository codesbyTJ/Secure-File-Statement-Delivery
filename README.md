# Secure-File-Statement-Delivery

A minimal service to store customer account statements (PDFs) and provide time-limited, secure download links to customers.

## Features
- User registration and login (JWT-based)
- Create time-limited download tokens for statements
- Serve statements as downloadable files via single-use / time-limited token links
- Simple web UI for onboarding, login and requesting downloads (Jinja2 templates)
- Docker + docker-compose for local development

## Architecture
- Backend: FastAPI (Python)
- DB: MySQL (production) with SQLite fallback for local dev
- File storage: local filesystem (statements_files/) -Swap for production
- Auth: JWT tokens for API, cookies for web UI
- Password hashing: passlib (argon2 / bcrypt_sha256 recommended)

## Quick start (Docker Compose)
1. Copy or update `.env` (example below).
2. From project root:
   - Build and start services:
     docker compose up -d --build
   - View logs:
     docker compose logs -f web
3. Open UI:
   - Register: http://localhost:8000/onboard
   - Login:    http://localhost:8000/login
   - Statements: http://localhost:8000/statements
   - Swagger: http://localhost:8000/docs

## Local development (no Docker)
1. Create and activate virtualenv:
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1   # Windows PowerShell
2. Install dependencies:
   python -m pip install -r requirements.txt
3. For quick start use SQLite:
   $env:DATABASE_URL = "sqlite:///./dev.db"   # PowerShell
   python -m uvicorn main:app --reload

## Environment variables
- DATABASE_URL (e.g. mysql+pymysql://user:pass@host/db or sqlite:///./dev.db)
- MYSQL_ROOT_PASSWORD, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD (used by docker-compose)
- SECRET_KEY / JWT settings (keep secret in production)
- TOKEN_TTL (optional - minutes for download tokens)

## Key endpoints
- POST /auth/register         — register (JSON: {email, password})
- POST /auth/login            — login (form: username(email), password) -> return access_token
- GET  /onboard               — web register page
- GET  /login                 — web login page
- GET  /statements            — web statement request page
- POST /statements/generate-download-json — create download token (returns token + expiration)
- POST /statements/generate-download-token — create download token (API)
- GET  /statements/download-statement/?token=<token> — download file using token

Use Authorization: Bearer <token> for protected API calls when not using the web UI.

## Database / Migrations
- Models are SQLAlchemy ORM.
- On startup, tables are auto-created: Base.metadata.create_all(bind=engine).

## File storage
- Default local folder: `statements_files/` (create and place PDFs with matching DB filenames).

## Security notes / recommendations
- Use HTTPS in production for security
- Use strong SECRET_KEY and rotate tokens if needed.
- Do not expose raw tokens in logs.
- For hashing prefer `argon2` or `bcrypt_sha256` (avoid raw bcrypt 72-byte limit).
- Validate user authorization on token creation (only owner of statement should be allowed).
- Consider single-use tokens (delete after first download) and audit logs.

## Testing
- Add unit tests for auth, token generation, and download flow.
- Use SQLite in-memory DB for fast tests.

## Contributing
- Fork, create feature branch, open PR with tests.

