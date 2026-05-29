# Contributing to SeniorMate

Thank you for helping improve SeniorMate. This guide defines the workflow for issues, branches, commits, pull requests, testing, documentation, and changelog updates.

## Code of Conduct

- Be respectful, collaborative, and professional.
- Use inclusive language.
- Do not harass, insult, or abuse other contributors.

## Getting Started

1. Start from a clean and current `main` branch.

   ```bash
   git checkout main
   git pull origin main
   ```

2. Create a focused branch for your change.
3. Follow the setup instructions in `README.md`.
4. Keep each pull request small enough to review safely.

## Branch Naming

Use short, descriptive branch names:

- `feature/<short-description>` for new features
- `fix/<short-description>` for bug fixes
- `docs/<short-description>` for documentation-only changes
- `chore/<short-description>` for maintenance work

Examples:

- `feature/patient-profile`
- `fix/login-validation`
- `docs/local-development`
- `chore/update-ci`

## Commit Messages

Use concise, imperative commit messages:

- `Add patient profile scaffold`
- `Fix visit note validation`
- `Update local development docs`

Reference issues when useful, for example `Fixes #123`.

## Pull Request Process

1. Rebase or update your branch with the latest `main` before opening a PR.
2. Fill out the pull request template completely.
3. Link the related issue, task, or decision record when one exists.
4. Keep the PR focused on one logical change.
5. Include screenshots for UI changes.
6. Confirm tests and checks were run, or explain why they were not applicable.
7. Request maintainer review.

Only the maintainer merges pull requests into `main`. Contributors and automation must not merge PRs unless explicitly authorized by the maintainer.

## Testing Expectations

- Run relevant backend, frontend, and Docker checks before submitting a PR.
- Add or update tests for new behavior and bug fixes.
- If a test suite is not available yet, document the manual validation performed in the PR.
- Do not mark a PR as fully tested if checks were skipped or unavailable.

## Changelog Requirement

Update `CHANGELOG.md` for every user-facing feature, bug fix, workflow change, documentation standard, or repository maintenance change that future contributors should know about.

Use the `Unreleased` section for work that has not been released yet.

## Documentation

Update `README.md`, files under `docs/`, or inline documentation when behavior, setup, architecture, or contributor workflow changes.

## Security

- Never commit secrets, credentials, private keys, production data, or real environment values.
- Use `.env.example` for safe placeholder values only.
- Report security concerns privately to the maintainer.
