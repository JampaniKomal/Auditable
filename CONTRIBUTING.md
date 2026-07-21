# Contributing to Auditable

Thanks for helping improve Auditable.

## Principles

- Keep additions focused on local training and compliance simulation.
- Preserve the intentionally vulnerable behavior of the scenarios unless a change is explicitly meant to improve repository quality or documentation.
- Favor small, reviewable commits.
- Add or update scenario-level audit guides when introducing new infrastructure.

## Recommended Workflow

1. Fork or branch from `main`.
2. Make the smallest change that solves the problem.
3. Validate the affected scenario with Docker Compose or a relevant syntax check.
4. Update documentation if the user-facing behavior changes.
5. Open a pull request with a clear summary of the change and any verification performed.

## Reporting Issues

- Use a concise title and include the scenario name.
- Provide the exact command, port, or file path involved.
- Include logs or screenshots when possible.