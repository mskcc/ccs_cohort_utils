#!/usr/bin/env python3
import asyncio
import os
import sys
from nats.aio.client import Client as NATS

async def send_test_message(target_id: str):
    nats_url = os.getenv("NATS_URL", "nats://127.0.0.1:4222")
    nc = NATS()
    await nc.connect(servers=[nats_url])
    print(f"Connected to NATS at {nats_url}")
    
    # Publish the raw target_id to the maf.send subject
    await nc.publish("maf.send", target_id.encode())
    await nc.flush()
    print(f"Published '{target_id}' to subject 'maf.send'")
    
    await nc.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sendTestMessage.py <target_id>")
        sys.exit(1)
    target_id = sys.argv[1]
    asyncio.run(send_test_message(target_id))

