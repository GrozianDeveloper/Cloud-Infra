# Gitea Runner

Goal: CI via Gitea Actions (`gitea-act-runner` catalog)

## Docs

- [Instance](../instance/gitea-runner/Readme.md)
- Gitea: [gitea/README.md](../gitea/README.md)

## Installation

- No published ports. Uses docker.sock.
- Requires Gitea Actions enabled (`GITEA__ACTIONS__ENABLED=true`)
- Token: `RUNNER_REGISTRATION_TOKEN` in `instance/gitea/.env`
- Pipelines: `gitea-runner/pipelines`
- One live runner. Offline duplicates — delete via `DELETE /api/v1/admin/actions/runners/{id}`
