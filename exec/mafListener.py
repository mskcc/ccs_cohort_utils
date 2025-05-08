#!/usr/bin/env python3
import asyncio
import os
from nats.aio.client import Client as NATS
from nats.js.client import JetStreamContext
from nats.js.manager import JetStreamManager

# ── Configuration ──────────────────────────────────────────────────────────────
BASE_DIR = "/juno/work/tempo/wes_repo/Results/v1.4.x/somatic"
STREAM   = "MAF"
SUBJECT  = "maf.send"
DURABLE  = "sendMafListener"
NATS_URL = os.getenv("NATS_URL", "nats://127.0.0.1:4222")
# ────────────────────────────────────────────────────────────────────────────────

async def run_send_maf(path: str):
    """Launch sendMaf.py, await its completion, and log success or error."""
    proc = await asyncio.create_subprocess_exec(
        "python3", "sendMaf.py", path,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode == 0:
        print(f"[sendMaf SUCCESS] {path}\n{stdout.decode().strip()}")
    else:
        print(f"[sendMaf ERROR exit {proc.returncode}] {path}\n{stderr.decode().strip()}")

async def message_handler(msg):
    """Callback for each JetStream message (payload = target_id)."""
    target_id   = msg.data.decode().strip()
    target_path = os.path.join(BASE_DIR, target_id) + os.sep

    print(f"[listener] received ID = {target_id}")
    print(f"[listener] resolved path = {target_path}")

    if not os.path.isdir(target_path):
        print("[listener] ERROR: path does not exist, skipping.")
        await msg.ack()
        return

    # fire-and-forget so we can ack immediately and keep listening
    asyncio.create_task(run_send_maf(target_path))
    await msg.ack()

async def main():
    #Instantiate and connect NATS client to server.
    nc = NATS()
    await nc.connect(servers=[NATS_URL])

    #Make a JetStreamManager with that connected client
    jsm = JetStreamManager(nc)

    #Make sure the stream exists (create if not)
    try:
        await jsm.stream_info(STREAM)
        print(f"[jetstream] stream '{STREAM}' already exists")
    except Exception:
        print(f"[jetstream] creating stream '{STREAM}' for subject '{SUBJECT}'")
        await jsm.add_stream(
            name=STREAM,
            subjects=[SUBJECT],
            storage="file",
            retention="limits"
        )

    #Grab a JetStream context and subscribe with a durable consumer
    js: JetStreamContext = nc.jetstream()
    await js.subscribe(
        SUBJECT,
        durable=DURABLE,
        cb=message_handler
    )

    print(f"Listening for messages on '{SUBJECT}' (stream={STREAM}, durable={DURABLE}) at {NATS_URL}")
    #Listen forever
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
