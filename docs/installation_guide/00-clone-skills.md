# Clone + skills

Repo-root. Do this before any TrueNAS API work.

## New instance vs this NAS

If `instance/truenas/.env` already has `TRUENAS_API_KEY` → this repo is a **live** NAS. Abort first-install unless the user said **new instance**.

New instance: copy [instance/_template/](../../instance/_template/Readme.md) into `instance/` (apps Readmes + maps YAML). Do not overwrite live `.env` or `instance/maps/**/apply*.py`. AI writes `instance/first-install-state.yaml` (no script).

## Skills

```bash
npx skills experimental_install
```

Lock: `skills-lock.json` (no `-g`). Custom skills stay in `.cursor/skills/` (TrueNAS, Authentik, Dockge, first-install).

Need Node 18+ and Python 3 on the agent machine.
