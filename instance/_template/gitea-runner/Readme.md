# Gitea Runner

- No published ports. docker.sock host mount.
- Data=`apps/gitea-runner`. Owner `568:568` (`apps`) or registration fails.
- Runner name: `truenas-runner` (labels `ubuntu-latest` / `ubuntu-24.04` / `ubuntu-22.04`)
- Token: `RUNNER_REGISTRATION_TOKEN` in `instance/gitea/.env`
