#!/bin/bash

# -----------------------------------------------
# Config
# -----------------------------------------------
NATS_HOST="localhost"
NATS_PORT="4222"
NATS_URL="nats://${NATS_HOST}:${NATS_PORT}"
STREAM_NAME="MDB_STREAM"
STREAM_SUBJECT="MDB_STREAM.>"

# -----------------------------------------------
# Help
# -----------------------------------------------
usage() {
    echo "Usage: $(basename "$0") [-h]"
    echo ""
    echo "Starts a local NATS server and creates the ${STREAM_NAME} JetStream stream."
    echo ""
    echo "Options:"
    echo "  -h    Show this help message and exit."
}

while getopts ":h" opt; do
    case "$opt" in
        h) usage; exit 0 ;;
        \?) echo "Error: Unknown option -$OPTARG" >&2; usage; exit 1 ;;
    esac
done

# -----------------------------------------------
# Check dependencies
# -----------------------------------------------
for cmd in nats-server nats; do
    if ! command -v "$cmd" &>/dev/null; then
        echo "Error: '$cmd' is not installed or not in PATH." >&2
        echo "  nats-server: https://docs.nats.io/running-a-nats-service/introduction/installation"
        echo "  nats CLI:    https://github.com/nats-io/natscli"
        exit 1
    fi
done

# -----------------------------------------------
# Start NATS server (if not already running)
# -----------------------------------------------
JETSTREAM_STORE_DIR="/tmp/nats-jetstream"

if nc -z "$NATS_HOST" "$NATS_PORT" 2>/dev/null; then
    echo "NATS server is already running on ${NATS_URL}."
else
    echo "Starting NATS server with JetStream enabled..."
    mkdir -p "$JETSTREAM_STORE_DIR"
    nats-server --jetstream --store_dir="$JETSTREAM_STORE_DIR" &
    NATS_PID=$!
    echo "NATS server started (PID: ${NATS_PID})"

    # Wait for it to become available
    echo -n "Waiting for NATS server to be ready"
    for i in $(seq 1 10); do
        if nc -z "$NATS_HOST" "$NATS_PORT" 2>/dev/null; then
            echo " ready."
            break
        fi
        echo -n "."
        sleep 0.5
        if [[ $i -eq 10 ]]; then
            echo ""
            echo "Error: NATS server did not start in time." >&2
            exit 1
        fi
    done
fi

# -----------------------------------------------
# Create stream if it doesn't already exist
# -----------------------------------------------
if nats --server="$NATS_URL" stream info "$STREAM_NAME" &>/dev/null; then
    echo "Stream '${STREAM_NAME}' already exists — skipping creation."
else
    echo "Creating stream '${STREAM_NAME}' with subject '${STREAM_SUBJECT}'..."
    nats --server="$NATS_URL" stream add "$STREAM_NAME" \
        --subjects="$STREAM_SUBJECT" \
        --defaults

    if [[ $? -eq 0 ]]; then
        echo "Stream '${STREAM_NAME}' created successfully."
    else
        echo "Error: Failed to create stream '${STREAM_NAME}'." >&2
        exit 1
    fi
fi

# -----------------------------------------------
# Confirm final state
# -----------------------------------------------
echo ""
echo "Stream info:"
nats --server="$NATS_URL" stream info "$STREAM_NAME"
