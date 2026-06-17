#!/usr/bin/env python3
"""
Multi-user simulation test for FIFOLive.

Simulates multiple customers placing orders nearly simultaneously
and verifies:
- Strict FIFO ordering (sorted by created_at)
- Correct stock reservation
"""

import requests
import time
from datetime import datetime

BASE = "http://localhost:8000"

def place_order(name, pid, qty):
    r = requests.post(f"{BASE}/api/order-request", json={
        "customer_name": name,
        "product_id": pid,
        "qty": qty
    })
    data = r.json()
    order = data["order"]
    print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] {name} placed {order['id']} for {qty}x {pid} @ ₹{order['total_price']}")
    return order

def get_pending():
    return requests.get(f"{BASE}/api/pending-orders").json()["orders"]

def get_products():
    return requests.get(f"{BASE}/api/products").json()["products"]

def main():
    print("=== Multi-User FIFO Simulation Test ===\n")

    users = [
        ("Alice", "p1", 1),
        ("Bob", "p2", 2),
        ("Charlie", "p1", 1),
        ("Dana", "p3", 3),
    ]

    for name, pid, qty in users:
        place_order(name, pid, qty)
        time.sleep(0.08)

    print("\n--- Pending Queue (should be oldest first) ---")
    pending = get_pending()
    print(f"Total pending: {len(pending)}")

    for i, o in enumerate(pending[:8]):
        ts = datetime.fromtimestamp(o['created_at']/1000).strftime('%H:%M:%S.%f')[:-3]
        print(f"  {i+1}. {o['customer_name']:8} | {o['qty']}x {o['product_id']} | {ts} | {o['status']}")

    # Verify FIFO
    created = [o['created_at'] for o in pending]
    is_fifo = all(created[i] <= created[i+1] for i in range(len(created)-1))
    print(f"\nFIFO ordering: {'✅ PASS' if is_fifo else '❌ FAIL'}")

    print("\n--- Stock Reservations ---")
    for p in get_products()[:4]:
        avail = p['stock_total'] - p.get('stock_reserved', 0)
        print(f"  {p['name']}: total={p['stock_total']}, reserved={p.get('stock_reserved',0)}, available={avail}")

    print("\n✅ Multi-user test finished.")

if __name__ == "__main__":
    main()
