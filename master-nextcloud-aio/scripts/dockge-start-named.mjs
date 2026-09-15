#!/usr/bin/env node
/** Start a Dockge stack and print its compose terminal. */
import { readFileSync } from "fs";
import { createRequire } from "module";
import { dirname, resolve } from "path";
import { fileURLToPath } from "url";

const require = createRequire(
  resolve(dirname(fileURLToPath(import.meta.url)), "../../.cursor/skills/truenas-scale/package.json"),
);
const { io } = require("socket.io-client");

const skillEnv = readFileSync(
  resolve(dirname(fileURLToPath(import.meta.url)), "../../.cursor/skills/truenas-scale/.env"),
  "utf8",
);
const creds = {};
for (const line of skillEnv.split("\n")) {
  const m = line.match(/^(DOCKGE_USER|DOCKGE_PASS)=(.*)$/);
  if (m) creds[m[1]] = m[2];
}

const stackName = process.argv[2];
if (!stackName || !creds.DOCKGE_USER) {
  console.error("Usage: dockge-start-named.mjs <stack>");
  process.exit(1);
}

const socket = io("http://192.168.0.35:31014", {
  transports: ["websocket"],
  reconnection: false,
});

socket.on("connect", () => {
  socket.emit(
    "login",
    { username: creds.DOCKGE_USER, password: creds.DOCKGE_PASS, token: "" },
    (r) => {
      if (!r || !r.ok) {
        console.error("Login failed");
        process.exit(1);
      }
      socket.emit("terminalJoin", `compose-${stackName}`);
      socket.emit("terminalJoin", `combined-${stackName}`);
      socket.onAny((event, ...args) => {
        if (event === "connect") return;
        const preview = JSON.stringify(args)?.slice(0, 800);
        if (preview && preview !== "[]") console.error("evt", event, preview);
      });
      setTimeout(() => {
        socket.emit("agent", "", "startStack", stackName, (resp) => {
          console.log(JSON.stringify(resp, null, 2));
          setTimeout(() => {
            socket.disconnect();
            process.exit(resp?.ok === false ? 1 : 0);
          }, 2500);
        });
      }, 800);
    },
  );
});

socket.on("connect_error", (err) => {
  console.error("Connection failed:", err.message);
  process.exit(1);
});

socket.on("terminalWrite", (name, data) => {
  const chunk = typeof data === "string" ? data : JSON.stringify(data);
  process.stderr.write(`[${name}] ${chunk}`);
});

setTimeout(() => {
  console.error("timeout");
  socket.disconnect();
  process.exit(1);
}, 120000);
