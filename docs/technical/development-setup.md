# Development Setup

Docker Compose is the supported full-stack development path.

## Requirements

- Git
- Docker with Compose
- Python 3.12 for backend-only work
- Node.js 20 for frontend-only work

## Start

```bash
git clone git@github.com:salimsaidhemed/SeniorMate.git
cd SeniorMate
cp .env.example .env
docker compose up --build
docker compose exec backend flask db upgrade
```

Open `http://localhost:5173`.

## Native Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
flask --app run:app run --debug
```

Set `DATABASE_URL` and `MINIO_ENDPOINT` to host-reachable services.

## Native Frontend

```bash
cd frontend
npm install
npm run dev
```

Set `VITE_API_BASE_URL` and the Keycloak variables before starting Vite.

For ports and troubleshooting, see
[Local Development](../setup/local-development.md).
