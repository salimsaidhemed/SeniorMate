# CI/CD Overview

GitHub Actions runs on every pull request and push to `main`.

## Backend CI

- Python 3.12
- pip dependency cache
- Ruff
- pytest

## Frontend CI

- Node.js 20
- npm dependency cache
- `npm ci` when the lockfile exists
- Vite production build

## Docker Build

- Validates Docker Compose configuration
- Builds backend and frontend images
- Does not push images

Workflows opt JavaScript actions into the Node.js 24 runtime and use current
major versions of checkout and setup actions.

## Release Boundary

The repository does not currently deploy automatically or push production
images. Deployment credentials and approval gates should be introduced only
with a documented target environment and maintainer approval.
