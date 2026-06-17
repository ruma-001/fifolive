# FIFOLive — FIFO Live Order Chat App

A production-ready prototype that lets YouTube, Instagram, and TikTok live sellers take orders directly in a clean, priority-based FIFO chat system — replacing the broken WhatsApp flow.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688)
![License](https://img.shields.io/badge/license-MIT-green)

## The Problem It Solves

Indian live sellers currently:
- Show a phone number on screen
- Ask viewers to "DM on WhatsApp"
- Get flooded with messages (newest on top)
- Spend hours scrolling to find the first real order
- Mix up inquiries vs. actual purchases
- Manually track stock

**FIFOLive fixes this**:
- Every order request is timestamped and locked in FIFO order.
- Stock is **reserved instantly** when the order is placed (first come = guaranteed allocation).
- Vendor dashboard always shows oldest orders at the top.
- Real-time updates across vendor + all customers.
- Real multi-method payments (UPI, Cards, Wallets, Razorpay Checkout).
- One source of truth for inventory.

## Features

- Strict FIFO order queue with locking
- Real-time WebSocket updates
- Realistic payments:
  - UPI (QR + VPA + app intents)
  - Debit/Credit Cards (with test failures)
  - Wallets (Paytm, PhonePe, Amazon Pay)
  - Full Razorpay test checkout integration
- Automatic receipts on success + PDF export
- Saved payment methods per customer
- Simulated live chat + bulk order testing
- Stock reservation and live sync

## Quick Start

### Requirements
- Python 3.10+

### Using the launcher (recommended)

```bash
git clone https://github.com/ruma-001/fifolive.git
cd fifolive

chmod +x run.sh
./run.sh
```

### Manual setup

```bash
git clone https://github.com/ruma-001/fifolive.git
cd fifolive

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python main.py
```

Open in browser: **http://localhost:8000**

## How to Demo (Recommended Flow)

1. Keep default view = **Vendor**.
2. Click the **Customer** button (top) to switch (or use a second tab).
3. As a Customer:
   - Click **REQUEST ORDER** on any product, or use "Quick Order".
   - Or type in Live Chat.
4. Watch the order instantly appear in the **FIFO Priority Queue** (top of the list).
5. Try the full payment flow (UPI / Cards / Wallets / Razorpay).
6. Use the failure test buttons in the Cards tab.
7. Check the receipt modal and saved methods list.

## Project Structure

```
fifolive/
├── main.py              # Full FastAPI + embedded SPA
├── requirements.txt
├── run.sh               # One-click launcher
├── README.md
├── .gitignore
├── fifolive.db          # SQLite (demo data)
├── static/              # (optional static assets)
└── templates/           # (optional templates)
```

## Configuration & Monetization

The app includes a built-in pricing modal for vendors:
- Free tier
- Growth (₹999/mo)
- Pro

You can customize this in the frontend code.

## Tech Stack

- FastAPI + Uvicorn
- WebSockets (real-time)
- SQLite
- Tailwind + Vanilla JS (no build step)

## Docker

Build and run with Docker:

```bash
# Build
docker build -t fifolive .

# Run
docker run -p 8000:8000 fifolive
```

Or with docker-compose:

```bash
docker-compose up --build
```

Visit http://localhost:8000

Note: The app seeds sample data on first run.

## Deploying Online for Testing

To make the app publicly accessible for others to test (without everyone needing local setup):

### Code Updates for Deployment (required)
The app must respect platform environment variables:
- `PORT` (most platforms set this; defaults to 8000).
- `DB_PATH` (for SQLite persistence via disk; defaults to `fifolive.db`).

These are already supported in the current code.

### Recommended: Render.com (Free tier, easy GitHub + Docker)
1. Push your code to GitHub (repo already set up).
2. Go to [render.com](https://render.com), sign up, "New > Web Service".
3. Connect your GitHub repo and select `fifolive`.
4. Runtime: **Docker** (uses existing Dockerfile).
5. Add a **Persistent Disk** (e.g. 1GB) mounted at `/data`.
6. Set Environment Variable: `DB_PATH=/data/fifolive.db`.
7. Deploy! Your app will be at `https://your-app.onrender.com`.

Test the full flows: customer orders, payments (Razorpay test mode works over the internet), vendor queue, etc.

### Alternatives
| Platform   | Why Good                          | Notes                          |
|------------|-----------------------------------|--------------------------------|
| Railway    | Easy GitHub, volumes, credits     | Free tier generous             |
| Fly.io     | Containers + volumes              | Free limited machines          |
| ngrok (temp) | Quick public tunnel            | Run locally: `ngrok http 8000` (not persistent) |
| Heroku     | Classic Python support         | Uses `Procfile` + `runtime.txt` (see dedicated section below) |

### Heroku Deployment (Specific Instructions)

Heroku is great for quick Python deploys. We provide:

- `Procfile`: `web: uvicorn main:app --host 0.0.0.0 --port $PORT`
- `runtime.txt`: Specifies Python 3.11

**Steps:**

1. Make sure you have the `Procfile` and `runtime.txt` in your repo (they are included).

2. Create a Heroku app:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

3. (Optional but recommended) Set the port explicitly if needed (Heroku provides `$PORT` automatically):
   ```bash
   heroku config:set PORT=8000
   ```

4. **Important: SQLite on Heroku**
   - Heroku's filesystem is **ephemeral**. The `fifolive.db` will be lost on every dyno restart or deploy.
   - For real testing with persistence:
     - Use a paid Heroku Postgres add-on and update the app to use PostgreSQL (future enhancement).
     - Or accept data loss between restarts for demo purposes.
   - Current app uses `DB_PATH` env var — you can experiment with it, but SQLite won't persist reliably.

5. Scale and open:
   ```bash
   heroku open
   ```

6. View logs:
   ```bash
   heroku logs --tail
   ```

**Notes for Heroku:**
- The app seeds initial products on first run (or when DB is empty).
- All demo features (FIFO, payments with test keys, WebSockets, receipts) work out of the box.
- Free dynos sleep after 30 minutes of inactivity.

Update any local `localhost:8000` references in docs/tests when sharing the live URL.

## Running Tests

```bash
# Start the app first
./run.sh

# In another terminal
python tests/test_multi_user.py
python tests/test_websocket.py
./tests/test_docker.sh
```

Note: `test_multi_user.py` and `test_websocket.py` require the `requests` package (`pip install requests`).

## License

MIT

---

Built to solve real problems for live sellers in India. Contributions welcome!

## How to Demo (Recommended Flow)

1. Keep default view = **Vendor**.
2. Click the **Customer** button (top) to switch (or use a second tab).
3. As a Customer:
   - Click **REQUEST ORDER** on any product, or use "Quick Order".
   - Or type in Live Chat (e.g. "ORDER 2 T-Shirt").
4. Watch the order instantly appear in the **FIFO Priority Queue** (top of the list).
5. As Vendor:
   - Click **ACCEPT + LOCK** on the top order.
   - Then **MARK PAID** (or switch to Customer view and click "PAY VIA UPI").
6. Complete with **FULFILL** — watch stock drop in real time everywhere.
7. Try ordering the same product with a second "customer" — the first one stays on top and has the stock locked.

Use the simulation buttons ("Simulate comment", "3 fast orders") to create a busy queue and prove FIFO priority.

## Core Features

- **True FIFO Queue**: Always sorted by creation time (oldest first). No "latest message on top" problem.
- **Automatic Reservation**: Placing an order immediately reserves stock. Later buyers see reduced availability.
- **Real-time Sync**: WebSockets push stock changes, new orders, status updates to everyone.
- **Realistic Multi-Method Payments**:
  - UPI: Dynamic QR + VPA entry + Intent buttons (GPay, PhonePe, Paytm)
  - Debit / Credit Cards: Professional form with formatting + test card support
  - Wallets: Paytm, PhonePe, Amazon Pay buttons
  - **Real Razorpay Checkout Integration**: Opens the official Razorpay test checkout supporting all methods (UPI/Card/Wallets/Netbanking). This is production-ready pattern.
- Payment details (method + metadata) stored with every order.

**Additional features added**:
- Failure scenarios testing (card declined, insufficient funds, expired) in the payment modal — orders marked `failed`.
- Automatic success receipt/invoice modal (with Print to PDF).
- Saved payment methods per customer (auto-saves on success, quick reuse in customer view).
- **Vendor Controls**:
  - Live inventory with reserved counts
  - Inline stock adjustment
  - Accept / Mark Paid / Fulfill / Cancel actions
- **Customer Experience**:
  - Clean product grid
  - My Orders panel with payment buttons
  - Live chat that feeds the order queue
- **Simulation Tools**: Great for demos and testing edge cases.
- **Persistence**: SQLite (fifolive.db) — data survives restarts.
- **Monetization Modal**: Realistic pricing tiers shown in-app.

## Data Model (Simplified)

- **products**: id, name, price, stock_total, stock_reserved
- **orders**: id, created_at, customer_name, product_id, qty, total_price, status (requested → accepted → paid → completed / cancelled)
- **messages**: live chat log

Available stock shown everywhere = `stock_total - stock_reserved`.

On fulfill: `stock_total -= qty`, `stock_reserved -= qty`.

## Monetization Strategy (Included)

Built-in modal shows three tiers:

- **Starter** — Free (50 orders/mo)
- **Growth** — ₹999/mo or ₹9,990/yr (unlimited + extras) ← Recommended
- **Pro Live** — ₹2,499/mo (teams + real integrations)

+ 1.5–1.99% platform fee on completed orders.

This model is designed to be:
- Easy to adopt
- High LTV via subscriptions
- Aligned with seller success (they pay more only when they sell more)

## Payments (New — Realistic)

FIFOLive now includes a full retail-grade payment experience:

**Available methods:**
- **UPI** — Dynamic QR code, editable VPA, quick launch for GPay / PhonePe / Paytm
- **Cards** — Debit & Credit. Formatted inputs, test card support (`4111 1111 1111 1111`)
- **Wallets** — Paytm, PhonePe, Amazon Pay
- **Razorpay Checkout (Recommended)** — The actual Razorpay test environment. Supports everything + bank transfers. Uses `rzp_test_*` keys.

When a payment succeeds:
- Order status → `paid`
- `payment_method` + `payment_details` saved (VPA, last4, wallet name, etc.)
- Vendor sees it instantly

In production, simply:
1. Replace the test Razorpay key with your live key
2. Add server-side signature verification in `/api/razorpay-verify`
3. Add webhook handling for reliability

All flows are built exactly the same way real Indian D2C and live commerce apps work.

## Production Roadmap Ideas

- Real authentication (vendor accounts + customer phone)
- Full production Razorpay / PhonePe / Paytm integration
- YouTube Live Chat + Instagram Graph comment ingestors
- Multi-item carts
- Order management + shipping label export
- Analytics dashboard + daily reports
- Mobile PWA + push notifications
- "Start Live Session" button with per-session fees

## Files

- `main.py` — Everything (FastAPI + WebSocket + embedded SPA)
- `fifolive.db` — SQLite database
- `.venv/` — Python environment

## Tech

- FastAPI + Uvicorn
- Native WebSockets
- SQLite (stdlib)
- Tailwind CSS via CDN + vanilla JS (no build step)

## License / Notes

This is a working prototype you can run locally, pitch, or extend into a real SaaS product.

Built to directly attack the "WhatsApp live selling" pain point in India.

---

Run it. Place a few orders. Watch the queue. This is the future of live commerce ordering.
