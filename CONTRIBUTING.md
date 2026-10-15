# Contributing

## Development setup

**Backend (Python 3.12+)**

```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8010
```

**Frontend (Node 22+)**

```bash
cd frontend
npm install
npm run dev
```

Vite proxies `/api` traffic to `http://127.0.0.1:8010`.

## Running tests

```bash
# Backend unit tests
cd backend
python -m unittest discover -s tests -v

# Frontend build check
cd frontend
npm run build
```

CI runs both on every pull request.

## Pull request guidelines

- Branch from `main`, one feature or fix per PR
- Keep commits atomic and describe what changed, not why
- Tests must pass before requesting review
- No direct pushes to `main`

All session data in examples and tests is synthetic.
