#!/usr/bin/env node
/**
 * Dockge: list or start a stack. Creds from skill .env (USER/PASS only); URL :31014.
 * Usage: node dockge-start.mjs list
 *        node dockge-start.mjs start <stackName>
 */
import { readFileSync } from "fs";
import { createRequire } from "module";
import { dirname, resolve } from "path";
import { fileURLToPath } from "url";

const require = createRequire(
  resolve(
    dirname(fileURLToPath(import.meta.url)),
    "../../truenas-scale/package.json",
  ),
);
const { io } = require("socket.io-client");

const skillEnv = readFileSync(
  resolve(
    dirname(fileURLToPath(import.meta.url)),
    "../../truenas-scale/.env",
  ),
  "utf8",
);
const creds = {};
for (const line of skillEnv.split("\n")) {
  const m = line.match(/^(DOCKGE_USER|DOCKGE_PASS)=(.*)$/);
  if (m) creds[m[1]] = m[2];
}

const DOCKGE_URL = "http://192.168.0.35:31014";
const cmd = process.argv[2];
const stackName = process.argv[3];
if (
  !cmd ||
  ((cmd === "start" || cmd === "status" || cmd === "get" || cmd === "down") &&
    !stackName) ||
  !creds.DOCKGE_USER
) {
  console.error("Usage: dockge-start.mjs list | start <n> | status <n> | get <n> | down <n>");
  process.exit(1);
}

const socket = io(DOCKGE_URL, { transports: ["websocket"], reconnection: false });
const timeoutMs = cmd === "start" || cmd === "down" ? 300000 : 20000;

socket.on("connect", () => {
  socket.emit(
    "login",
    { username: creds.DOCKGE_USER, password: creds.DOCKGE_PASS, token: "" },
    (r) => {
      if (!r || !r.ok) {
        console.error("Login failed:", r?.msg || "no response");
        process.exit(1);
      }
      if (cmd === "list") {
        socket.emit("stackList");
        return;
      }
      if (cmd === "get") {
        socket.emit("agent", "", "getStack", stackName, (resp) => {
          if (resp?.stack) {
            const s = { ...resp.stack };
            if (typeof s.composeENV === "string") {
              s.composeENV = s.composeENV.replace(
                /^(.*(?:KEY|PASS|SECRET|TOKEN).*=).*$/gim,
                "$1***",
              );
            }
            console.log(JSON.stringify({ ok: resp.ok, stack: s }, null, 2));
          } else {
            console.log(JSON.stringify(resp, null, 2));
          }
          socket.disconnect();
          process.exit(resp?.ok === false ? 1 : 0);
        });
        return;
      }
      if (cmd === "status") {
        socket.emit("agent", "", "appStatusList", stackName, (resp) => {
          console.log(JSON.stringify(resp, null, 2));
          socket.disconnect();
          process.exit(resp?.ok === false ? 1 : 0);
        });
        return;
      }
      if (cmd === "down") {
        socket.emit("agent", "", "downStack", stackName, (resp) => {
          console.log(JSON.stringify(resp, null, 2));
          socket.disconnect();
          process.exit(resp?.ok === false ? 1 : 0);
        });
        return;
      }
      console.error("Starting", stackName);
      socket.emit("terminalJoin", "compose-caddy");
      socket.emit("terminalJoin", "combined-caddy");
      socket.emit("agent", "", "startStack", stackName, (resp) => {
        console.log(JSON.stringify(resp, null, 2));
        socket.disconnect();
        process.exit(resp?.ok === false ? 1 : 0);
      });
    },
  );
});

socket.on("connect_error", (err) => {
  console.error("Connection failed:", err.message);
  process.exit(1);
});

socket.on("agent", (eventType, data) => {
  if (eventType === "stackList" && cmd === "list") {
    if (!data || !data.ok) {
      console.error("stackList failed:", data?.msg);
      process.exit(1);
    }
    console.log(
      JSON.stringify(
        Object.entries(data.stackList || {}).map(([name, v]) => ({
          name,
          status: v.status,
          state: v.status === 3 ? "running" : "stopped",
        })),
        null,
        2,
      ),
    );
    socket.disconnect();
    process.exit(0);
  }
  if (eventType === "terminal" || eventType === "info") {
    const chunk = typeof data === "string" ? data : JSON.stringify(data);
    if (chunk) console.error(eventType, chunk.slice(0, 400));
  }
});

socket.on("terminalWrite", (name, data) => {
  const chunk = typeof data === "string" ? data : JSON.stringify(data);
  process.stderr.write(chunk);
});

socket.onAny((event, ...args) => {
  if (event === "agent" || event === "connect" || event === "terminalWrite") return;
  const preview = JSON.stringify(args)?.slice(0, 400);
  if (preview && preview !== "[]") console.error("evt", event, preview);
});

setTimeout(() => {
  console.error("Timeout after", timeoutMs, "ms");
  process.exit(1);
}, timeoutMs);
