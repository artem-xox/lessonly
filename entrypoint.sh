#!/usr/bin/env sh
set -e

PORT="${PORT:-8501}"

exec streamlit run src/lessonly/interfaces/app/main.py \
  --server.port "$PORT" \
  --server.address 0.0.0.0 \
  --browser.gatherUsageStats false \
  --server.headless true
