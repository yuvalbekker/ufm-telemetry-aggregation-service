#!/bin/bash
set -e

if [ "$MODE" = "API" ]; then
    echo "Starting API server..."
    exec uvicorn app.main:app --host 0.0.0.0 --port 8080
elif [ "$MODE" = "COUNTERS" ]; then
    echo "Starting Counters server..."
    exec uvicorn counters.main:counters --host 0.0.0.0 --port 9001
elif [ "$MODE" = "WORKER" ]; then
    echo "Starting worker process..."
    exec python -m app.ingestion.worker
else
    echo "Error: MODE environment variable must be set to 'API' or 'WORKER'."
    exit 1
fi