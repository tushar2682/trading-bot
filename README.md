# trading-n8n — Trading Automation Bot

A modular trading automation project with a Flask backend and a Vite/React frontend. The backend includes JWT authentication, workflow orchestration, trade management, portfolio analytics, and optional realtime SocketIO updates. The frontend UI for monitoring and interacting with the system is in `Frontend/trading-dashboard`.

---

## Repository layout

- `Backend/` — Flask backend application (models, routes, services, run script).
- `Frontend/trading-dashboard` — Frontend (Vite + React) application.

---

## Features

- User authentication using JWT (access & refresh tokens) with Redis-backed blocklist.
- Workflow creation, activation and execution for trading automation.
- Trade order management (create, cancel, history) and P&L tracking.
- Portfolio analytics and summary (unrealized & realized P&L, positions value).
- Realtime updates via SocketIO (optional module).

---

## Quickstart — Backend (Windows PowerShell)

1. Activate the virtual environment (adjust path if different):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
.\Backend\venv\Scripts\Activate.ps1
```

2. Install Python dependencies (if not already installed):

```powershell
pip install -r Backend\requirements.txt
```

3. Set essential environment variables (example):

```powershell
$env:JWT_SECRET_KEY = 'change-this-to-a-secure-value'
# Optional: $env:DATABASE_URL, $env:REDIS_URL
```

4. Start the backend (development):

```powershell
python Backend\run.py
```

Notes:

- To improve SocketIO support locally, install `eventlet` (`pip install eventlet`).
- By default the app factory will create DB tables on startup in a development context. For production, manage migrations (Alembic/Flask-Migrate).

---

## Quickstart — Frontend

```powershell
cd Frontend\trading-dashboard
npm install
npm run dev   # or npm start if configured
```

Set the frontend to point at the backend API (usually `http://localhost:5000`).

---

## Configuration

Primary backend configuration can be provided via `Backend/app/config.py` or environment variables:

- `JWT_SECRET_KEY` (required) — secret for signing JWTs.
- `SQLALCHEMY_DATABASE_URI` or `DATABASE_URL` — database connection string.
- `REDIS_URL` — Redis connection string (optional but recommended for token blocklist).

Create a `.env.example` with recommended settings for development.

---

## API Reference (selected endpoints)

All API routes are under `/api`.

### Auth (`/api/auth`)

- `POST /register` — Register user. Body: `{ email, username, password }`.
- `POST /login` — Login and return access & refresh tokens.
- `POST /logout` — Logout (blacklist current token).
- `POST /refresh` — Exchange refresh token for a new access token.
- `GET /me` — Get current user profile.

### Workflows (`/api/workflows`)

- `GET /` — List user's workflows.
- `POST /` — Create workflow.
- `GET/PUT/DELETE /:id` — Manage workflow by id.
- `POST /:id/execute` — Run a workflow manually.
- `POST /:id/activate` — Activate and schedule execution (background task).

### Trades (`/api/trades`)

- `GET /` — List trades (filters: symbol, status, pagination).
- `POST /` — Create a trade (body: `symbol, side, type, quantity[, price]`).
- `POST /:id/cancel` — Cancel a trade.

See the route implementations in `Backend/app/routes` for full request/response details.

---

## Development & Testing

- Use an API client like Postman or Insomnia to exercise endpoints during development.
- Recommended tools: `pytest`, `flake8`, `black` for testing and formatting.

```powershell
pip install pytest flake8 black
pytest
```

---

## Deployment suggestions

- Dockerize the backend and frontend with `Dockerfile` and `docker-compose.yml` (backend + redis + database).
- Use a production WSGI server (gunicorn/uvicorn) behind a reverse proxy, and a worker for SocketIO (eventlet/gevent).
- Use environment variables or secret manager for `JWT_SECRET_KEY` and DB credentials.

---

## Contributing

- Fork the repo and create a feature branch.
- Run tests and format code before opening a PR.

---


---

If you'd like, I can also:

- create a `.env.example` and a minimal `Backend/app/config.py` template,
- add a `/health` endpoint to the backend,
- create `Dockerfile` and `docker-compose.yml` for local dev.

Tell me which one you want next and I'll implement it.
- Add CI (GitHub Actions) to run tests and linting on PRs.

---

**Contributing**
- Fork the repo, create a feature branch, run tests, and open a PR with a clear description of changes.

---


If you want, I can also:
- Add an example `app/config.py` or `.env.example` with recommended settings.
- Add a small health-check endpoint to the backend.
- Create a `Dockerfile` and `docker-compose.yml` for local development.

Let me know which of those you'd like next and I will implement it.
