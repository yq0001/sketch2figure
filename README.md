# Sketch2Figure

![CI](https://github.com/OWNER/REPO/actions/workflows/ci.yml/badge.svg)

Replace `OWNER/REPO` with your GitHub repository path to enable the badge.

Sketch2Figure is a private, cross-platform web application for turning rough hand-drawn scientific sketches into polished scientific figures while preserving scientific meaning and version lineage.

**Current implementation: Phase 0 — Repository and architecture.**

The application launches, reports backend health/provider capabilities, has a migrated SQLite metadata schema, and includes a minimal React shell. Project creation, uploads, Vanilla image processing, and AI provider calls are intentionally not implemented until their assigned phases.

## Architecture

- **Frontend:** React + TypeScript + Vite + TanStack Query
- **Backend:** Python 3.12+ + FastAPI + Pydantic Settings + SQLAlchemy 2 + Alembic
- **Metadata:** SQLite
- **Assets:** filesystem abstraction (actual upload workflow arrives in Phase 1)
- **Image foundations:** Pillow + OpenCV + NumPy, installed now for Phase 1
- **AI providers:** backend-only provider abstraction for OpenAI, Gemini, and Claude; no SDK/API calls in Phase 0
- **Deployment:** Docker Compose with an Nginx frontend/reverse proxy and persistent backend data volume

Provider keys are never needed by the browser. Model IDs are configured through environment variables rather than scattered through application code.

## Prerequisites

### Windows development — Anaconda/conda recommended

Install:

- Anaconda or Miniconda/Miniforge with `conda` available
- Git
- VS Code

The included `environment.yml` installs **Python 3.12** and **Node.js 22** from conda-forge into a dedicated `sketch2figure` environment. You therefore do not need a separate system Python or Node.js installation for the recommended Windows workflow.

Docker Desktop is optional for ordinary development.

### Linux development/server

Install Python 3.12+, Node.js 22+, and optionally Docker Engine + Docker Compose.

## Environment setup

### Recommended Windows conda environment

From the repository root in **Anaconda Prompt** or a PowerShell terminal where `conda` has been initialized:

```powershell
conda env create -f environment.yml
conda activate sketch2figure
python -m pip install -r backend/requirements-dev.txt
Copy-Item .env.example .env
```

The `environment.yml` intentionally contains the development runtime (Python, pip, and Node.js), while Python application packages remain in `backend/requirements.txt` and `backend/requirements-dev.txt`. This avoids maintaining two competing dependency lists.

If the environment already exists, update the runtime definition and then refresh Python packages:

```powershell
conda env update -f environment.yml --prune
conda activate sketch2figure
python -m pip install -r backend/requirements-dev.txt
```

### Using an existing conda environment

If you prefer to keep using an existing Anaconda environment, activate it first and verify that it provides Python 3.12+ and Node.js 22+:

```powershell
conda activate YOUR_ENV_NAME
python --version
node --version
npm --version
python -m pip install -r backend/requirements-dev.txt
Copy-Item .env.example .env
```

If the existing environment contains unrelated scientific packages, a dedicated `sketch2figure` environment is safer because web/backend dependencies can otherwise conflict with packages used by other projects.

For Phase 0, provider API keys and image model IDs may remain blank. The backend will report OpenAI/Gemini as not configured and Claude raster generation as not enabled for this phase.

Important variables:

```text
APP_NAME=Sketch2Figure
APP_ENV=development
APP_HOST=127.0.0.1
APP_PORT=8000
FRONTEND_ORIGIN=http://localhost:5173
DATABASE_URL=sqlite:///./data/sketch2figure.db
DATA_DIR=./data
MAX_UPLOAD_MB=25
OPENAI_API_KEY=
OPENAI_IMAGE_MODEL=
GEMINI_API_KEY=
GEMINI_IMAGE_MODEL=
ANTHROPIC_API_KEY=
CLAUDE_IMAGE_MODEL=
RUN_EXTERNAL_AI_TESTS=0
```

Keep `.env` private. It is ignored by Git.

## Windows: run the backend with conda

Open Anaconda Prompt or PowerShell in `sketch2figure`:

```powershell
conda activate sketch2figure
New-Item -ItemType Directory -Force data | Out-Null
cd backend
python -m alembic upgrade head
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

If you chose an existing conda environment instead, replace `sketch2figure` with that environment name. Using `python -m ...` ensures Alembic and Uvicorn come from the currently activated conda interpreter rather than another Python installation on Windows.

Backend endpoints:

- `http://127.0.0.1:8000/api/health`
- `http://127.0.0.1:8000/api/providers`
- `http://127.0.0.1:8000/docs`

The development server binds only to localhost by default.

## Windows: run the frontend

In a second Anaconda Prompt/PowerShell window, activate the same environment first:

```powershell
conda activate sketch2figure
cd frontend
npm install
npm run dev
```

If you use another conda environment name, activate that environment instead. Node.js and npm are supplied by the recommended conda environment.

Open `http://localhost:5173`.

Vite proxies `/api` requests to the backend at `127.0.0.1:8000`.

## Linux local development

Linux may use either conda or a standard Python virtual environment. The application does not depend on conda at runtime.

Backend with standard Python tooling:

```bash
cd backend
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m alembic upgrade head
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## Tests and linting

Backend (from an activated conda environment):

```powershell
conda activate sketch2figure
cd backend
python -m ruff check .
python -m pytest
```

Frontend:

```powershell
conda activate sketch2figure
cd frontend
npm run lint
npm test
npm run build
```

Paid external AI tests must never run by default. Later integration tests will require explicit `RUN_EXTERNAL_AI_TESTS=1`.

## Docker

Docker is not required for normal Windows development.

Create `.env`, then from the repository root:

```powershell
docker compose up --build
```

Open `http://localhost:8080`.

The Compose frontend port is bound to `127.0.0.1`, keeping the development deployment local to the machine. SQLite and future image assets live in the persistent `sketch2figure_data` volume.

Stop with:

```powershell
docker compose down
```

Use `docker compose down -v` only when you intentionally want to delete persistent Docker data.

## Database and migrations

Metadata is managed with SQLAlchemy and Alembic. The initial migration creates:

- projects
- assets
- versions with parent-child lineage
- provider runs
- labels
- ratings

Create future migrations from `backend/` after activating the conda environment:

```powershell
conda activate sketch2figure
cd backend
python -m alembic revision --autogenerate -m "describe change"
python -m alembic upgrade head
```

Do not store image bytes in SQLite. Assets will be stored on disk and referenced by metadata records.

## Project structure

```text
sketch2figure/
  frontend/
    src/
      api/
      canvas/
      components/
      hooks/
      pages/
      styles/
      types/
  backend/
    alembic/
      versions/
    app/
      api/
      core/
      db/
      models/
      schemas/
      services/
        exports/
        prompts/
        providers/
        storage/
        vanilla/
    tests/
  data/
  docker/
  environment.yml
  .env.example
  .gitignore
  docker-compose.yml
  README.md
```

## Phase 0 engineering choices

1. **Synchronous SQLAlchemy for MVP simplicity.** SQLite and this initial single-user workload do not justify async database complexity. Provider calls can still be asynchronous.
2. **Alembic from the beginning.** The metadata schema will evolve materially across later phases, so migrations start now.
3. **Filesystem assets behind an abstraction.** This keeps local development simple and leaves a clean path to S3/object storage later.
4. **Provider capability contracts before provider SDKs.** UI/backend code can reason about raster generation/editing without coupling itself to vendor response formats.
5. **No hard-coded provider model IDs.** Provider model settings live in `.env`.
6. **Prompt rules are centralized.** Phase 0 includes style/fidelity prompt foundations; provider-specific prompt construction comes with provider integration.
7. **Claude is not faked.** Phase 0 leaves raster capability disabled and explicitly defers current API verification to Phase 4.
8. **Original source immutability is a data-model invariant for later phases.** Phase 1 will create derived versions instead of modifying an original asset.

## Common troubleshooting

### VS Code uses the wrong Python interpreter

Press `Ctrl+Shift+P` → **Python: Select Interpreter** and select the Python interpreter from the `sketch2figure` conda environment. Then open a new VS Code terminal and verify:

```powershell
conda activate sketch2figure
python -c "import sys; print(sys.executable)"
```

The printed path should point into the selected conda environment.

### `conda activate` does not work in PowerShell

Run the following once from Anaconda Prompt, then restart PowerShell/VS Code:

```powershell
conda init powershell
```

If your organization restricts PowerShell profile changes, use **Anaconda Prompt** instead.

### Python package seems installed but the backend cannot import it

This usually means `pip` and `python` are coming from different environments. Activate the intended conda environment and use `python -m pip` rather than bare `pip`:

```powershell
conda activate sketch2figure
python -m pip --version
python -m pip install -r backend/requirements-dev.txt
```

### Frontend says backend is checking/offline

Confirm the backend is running on `127.0.0.1:8000` and verify `/api/health` directly.

### SQLite database cannot be created

Run commands from the documented repository/backend locations and ensure the repository `data/` directory is writable. The application uses `pathlib`-compatible paths and does not depend on Windows-only separators.

### CORS errors

For normal Vite development, use `http://localhost:5173`. If you intentionally change the frontend origin, update `FRONTEND_ORIGIN` in `.env`.

### Provider shows Not configured

This is expected in Phase 0 when its API key or model setting is blank. Do not add secrets to frontend environment files.

## Next phase

**Phase 1 — Projects, upload, Original and Vanilla** will add project CRUD, validated PNG/JPEG/WebP uploads, camera-compatible upload handling, checksum-protected original assets, image preview/version navigation, a conventional Pillow/OpenCV/NumPy Vanilla cleanup pipeline, and tests for image validation/path safety/version lineage. It will not call generative AI.
