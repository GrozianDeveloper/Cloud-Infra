#!/usr/bin/env bash
# Fetch official gitea-mcp binary into .cursor/mcp/bin (gitignored)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
BINDIR="$ROOT/.cursor/mcp/bin"
VER="${GITEA_MCP_VERSION:-v1.7.0}"
os="$(uname -s)"
arch="$(uname -m)"
case "$os-$arch" in
  Darwin-arm64) asset="gitea-mcp_Darwin_arm64.tar.gz" ;;
  Darwin-x86_64) asset="gitea-mcp_Darwin_x86_64.tar.gz" ;;
  Linux-aarch64|Linux-arm64) asset="gitea-mcp_Linux_arm64.tar.gz" ;;
  Linux-x86_64) asset="gitea-mcp_Linux_x86_64.tar.gz" ;;
  *) echo "unsupported $os $arch" >&2; exit 1 ;;
esac
mkdir -p "$BINDIR"
tmp="$(mktemp)"
url="https://gitea.com/gitea/gitea-mcp/releases/download/${VER}/${asset}"
curl -fL --retry 3 --max-time 90 -o "$tmp" "$url"
tar -xzf "$tmp" -C "$BINDIR" gitea-mcp
chmod +x "$BINDIR/gitea-mcp"
rm -f "$tmp"
echo "installed $BINDIR/gitea-mcp ($VER $asset)"
