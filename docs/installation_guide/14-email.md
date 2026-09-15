# Shared SMTP

One file: `instance/email/.env`. Used by Authentik, Nextcloud mail, Gitea, n8n, Postiz, Caddy ACME (`ACME_EMAIL` may also be in `instance/caddy/.env`).

## Keys (no values in docs)

`SMTP_HOST`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`, `SMTP_Security` (`SSL` / `TLS`).

Template keys: [instance/_template/email/Readme.md](../../instance/_template/email/Readme.md).
