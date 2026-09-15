#!/usr/bin/env bash
# Recreate Caddy stack (needed after .env / compose changes). Brief edge blip.
# Usage: bash caddy/scripts/restart.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
node <<'JS'
import { readFileSync } from "fs";
import { createRequire } from "module";
import { resolve } from "path";
const require = createRequire(resolve(".cursor/skills/truenas-scale/package.json"));
const { io } = require("socket.io-client");
const skillEnv = readFileSync(".cursor/skills/truenas-scale/.env", "utf8");
const creds = {};
for (const line of skillEnv.split("\n")) {
  const m = line.match(/^(DOCKGE_USER|DOCKGE_PASS)=(.*)$/);
  if (m) creds[m[1]] = m[2];
}
const yaml = readFileSync("caddy/docker-compose.yml", "utf8");
const env = readFileSync("instance/caddy/.env", "utf8");
const socket = io("http://192.168.0.35:31014", { transports: ["websocket"], reconnection: false });
socket.on("connect", () => {
  socket.emit("login", { username: creds.DOCKGE_USER, password: creds.DOCKGE_PASS, token: "" }, (r) => {
    if (!r?.ok) { console.error("login fail"); process.exit(1); }
    socket.emit("terminalJoin", "compose-caddy");
    socket.emit("terminalJoin", "combined-caddy");
    // restartStack keeps old container env; deploy recreates with .env
    socket.emit("agent", "", "deployStack", "caddy", yaml, env, false, (resp) => {
      console.log(JSON.stringify({ ok: resp?.ok, msg: resp?.msg }, null, 2));
      socket.disconnect();
      process.exit(resp?.ok === false ? 1 : 0);
    });
  });
});
socket.on("terminalWrite", (_n, data) => {
  const chunk = typeof data === "string" ? data : JSON.stringify(data);
  if (chunk) process.stderr.write(chunk);
});
setTimeout(() => { console.error("timeout"); process.exit(1); }, 180000);
JS
