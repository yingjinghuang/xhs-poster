#!/bin/bash
set -euo pipefail

export PATH="${HOME:-}/.local/share/fnm/aliases/default/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:${PATH:-}"

APP_DIR="$(cd "$(dirname "$0")" && pwd)"
PORT_CANDIDATES=(3000 3001 3002 3003 3004 3005)

cd "$APP_DIR"

if ! command -v npm >/dev/null 2>&1; then
  echo "没有找到 npm。请先安装 Node.js，再启动小红书卡片工具。"
  exit 1
fi

app_is_ready() {
  local port="$1"
  curl -fsS --max-time 2 "http://localhost:${port}" 2>/dev/null | grep -Eq "LuKK XHS Poster Studio|文章进来"
}

port_is_busy() {
  local port="$1"
  lsof -nP -iTCP:"${port}" -sTCP:LISTEN >/dev/null 2>&1
}

for port in "${PORT_CANDIDATES[@]}"; do
  if app_is_ready "$port"; then
    open "http://localhost:${port}"
    exit 0
  fi
done

PORT=""
for port in "${PORT_CANDIDATES[@]}"; do
  if ! port_is_busy "$port"; then
    PORT="$port"
    break
  fi
done

if [ -z "$PORT" ]; then
  echo "3000-3005 端口都被占用，无法启动小红书卡片工具。"
  exit 1
fi

URL="http://localhost:${PORT}"
NEXT_LOG="/tmp/xhs-poster-next-${PORT}.log"
BUILD_LOG="/tmp/xhs-poster-build.log"

if [ ! -f ".next/BUILD_ID" ]; then
  npm run build >"$BUILD_LOG" 2>&1 || {
    echo "小红书卡片工具构建失败。日志：${BUILD_LOG}"
    exit 1
  }
fi

nohup ./node_modules/.bin/next start --port "$PORT" >"$NEXT_LOG" 2>&1 &
SERVER_PID=$!
disown "$SERVER_PID" >/dev/null 2>&1 || true

for _ in {1..45}; do
  if app_is_ready "$PORT"; then
    open "$URL"
    exit 0
  fi

  if ! kill -0 "$SERVER_PID" >/dev/null 2>&1; then
    echo "小红书卡片工具启动失败。日志：${NEXT_LOG}"
    exit 1
  fi

  sleep 1
done

echo "小红书卡片工具启动超时。日志：${NEXT_LOG}"
exit 1
