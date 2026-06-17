#!/usr/bin/env python3
"""
WebSocket test for FIFOLive.

Connects to /ws, receives init, triggers an order via HTTP,
and verifies that broadcast messages (new_order, stock_update) arrive.
"""

import asyncio
import websockets
import json
import requests

BASE = "http://localhost:8000"
WS_URL = "ws://localhost:8000/ws"

async def test():
    print("=== WebSocket Broadcast Test ===\n")

    print("Connecting to WS...")
    async with websockets.connect(WS_URL) as ws:
        init = json.loads(await ws.recv())
        print(f"Received init: {len(init.get('products', []))} products, "
              f"{len(init.get('pending_orders', []))} pending")

        print("\nPlacing order via HTTP to trigger broadcast...")
        r = requests.post(f"{BASE}/api/order-request", json={
            "customer_name": "WSTestUser",
            "product_id": "p1",
            "qty": 1
        })
        print(f"HTTP placed: {r.json()['order']['id']}")

        print("\nWaiting for broadcast (up to 5s)...")
        try:
            msg = await asyncio.wait_for(ws.recv(), timeout=5.0)
            data = json.loads(msg)
            print(f"Received on WS: {data.get('type')}")
            if data.get('type') == 'new_order':
                o = data['order']
                print(f"  ✅ new_order from {o['customer_name']} for {o['qty']}x {o['product_id']}")
                print("WebSocket broadcast: ✅ PASS")
            else:
                print(f"  Got unexpected type: {data}")
        except asyncio.TimeoutError:
            print("  ❌ No broadcast received (timeout)")
            print("WebSocket broadcast: ❌ FAIL (check if server was restarted after the broadcast fix)")

    print("\n✅ WebSocket test finished.")

if __name__ == "__main__":
    asyncio.run(test())
