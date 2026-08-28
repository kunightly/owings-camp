#!/bin/bash
set -e
PROJECT_DIR="/root/owings-camp"
cd "$PROJECT_DIR"
echo "===== $(date) ====="
echo "[1/2] Pulling latest code..."
git pull origin main
echo "[2/2] Running debt notifier..."
python3 main.py
echo "Finished."