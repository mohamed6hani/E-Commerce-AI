"""Add a repeatable synthetic storefront dataset without replacing existing data.

Run from any directory: python tools/seed_demo_data.py
Uses only Python's standard library. The app must have initialized its SQLite
schema first. Demo records are tracked separately so reruns do not duplicate them.
"""

import json
import sqlite3
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATABASE = ROOT / "backend-mern" / "data" / "ecommerce.sqlite"
DEMO_PASSWORD = "DemoStore2026!"

PRODUCTS = [
    ("headphones", "Aero Wireless Headphones", "Electronics", "89.90", 24,
     "Comfortable over-ear headphones with noise isolation and 30-hour battery life."),
    ("keyboard", "Studio Mechanical Keyboard", "Office", "69.00", 18,
     "Compact keyboard with tactile switches, quiet stabilizers and USB-C connectivity."),
    ("lamp", "Halo LED Desk Lamp", "Home & Kitchen", "34.50", 32,
     "Adjustable desk lighting with three color temperatures and a dimmable touch control."),
    ("watch", "Pulse Smartwatch", "Electronics", "129.00", 3,
     "Everyday activity tracker with a bright display, heart-rate tracking and five-day battery."),
    ("mat", "Flow Yoga Mat", "Fitness", "24.00", 40,
     "Non-slip, cushioned exercise mat for stretching, yoga and home workouts."),
    ("bottle", "Trail Insulated Bottle", "Fitness", "19.50", 50,
     "Reusable 750 ml stainless-steel bottle that keeps drinks cold during busy days."),
    ("backpack", "Metro Commuter Backpack", "Lifestyle", "54.00", 14,
     "Lightweight backpack with a padded laptop compartment and water-resistant finish."),
    ("mug", "Terra Ceramic Mug Set", "Home & Kitchen", "28.00", 22,
     "Two handcrafted-style ceramic mugs with a matte finish for coffee and tea."),
    ("hub", "Connect USB-C Hub", "Accessories", "39.00", 0,
     "Six-port travel hub with HDMI, USB-A and card slots; currently awaiting replenishment."),
    ("charger", "Orbit Wireless Charging Pad", "Accessories", "29.00", 28,
     "Compact 15W charging pad with a non-slip base and a soft status light."),
    ("stand", "Lift Aluminum Laptop Stand", "Office", "44.00", 16,
     "Foldable aluminum stand that raises your screen and improves desk ergonomics."),
    ("organizer", "Canvas Everyday Organizer", "Lifestyle", "22.00", 35,
     "Small zip pouch for cables, stationery and daily essentials, made from durable canvas."),
]

CUSTOMERS = ["Maya Hassan", "Omar Nabil", "Lina Farouk", "Adam Saleh",
             "Nora Adel", "Youssef Karim", "Salma Amin", "Hana Mostafa"]

# Values are product keys and quantities; totals use the catalog unit prices.
ORDER_ITEMS = [
    [("headphones", 1), ("charger", 1)],
    [("mat", 1), ("bottle", 2)],
    [("keyboard", 1), ("stand", 1), ("lamp", 1)],
    [("backpack", 1), ("organizer", 1)],
    [("watch", 1), ("bottle", 1)],
    [("mug", 2), ("lamp", 1)],
    [("headphones", 1), ("keyboard", 1)],
    [("stand", 2), ("organizer", 1)],
    [("mat", 2), ("bottle", 2)],
    [("backpack", 1), ("charger", 1), ("organizer", 1)],
    [("watch", 1), ("headphones", 1)],
    [("mug", 1), ("lamp", 2)],
    [("keyboard", 1), ("charger", 1)],
    [("stand", 1), ("bottle", 1), ("organizer", 1)],
    [("headphones", 2), ("charger", 2)],
    [("watch", 1), ("backpack", 1), ("organizer", 1)],
]
STATUSES = ["delivered"] * 8 + ["shipped"] * 4 + ["processing"] * 2 + ["pending"] * 2


def seed():
    if not DATABASE.is_file():
        raise SystemExit("Start the Node backend once before seeding the demo database.")
    connection = sqlite3.connect(DATABASE, timeout=30)
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sqlite3.Row
    required = {"users", "products", "orders", "order_items", "reviews"}
    tables = {r[0] for r in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    if not required.issubset(tables):
        connection.close()
        raise SystemExit("The app schema is incomplete. Start the Node backend before seeding.")

    # Preserve a consistent pre-seed backup once; later reruns leave it intact.
    backup = ROOT / "tmp" / "demo-data" / "ecommerce-before-demo.sqlite"
    backup.parent.mkdir(parents=True, exist_ok=True)
    if not backup.exists():
        with sqlite3.connect(backup) as destination:
            connection.backup(destination)

    inserted = {name: 0 for name in sorted(required)}
    try:
        connection.execute("BEGIN IMMEDIATE")
        connection.execute("""CREATE TABLE IF NOT EXISTS demo_seed_records (
            entity TEXT NOT NULL, demo_key TEXT NOT NULL, record_id INTEGER NOT NULL,
            PRIMARY KEY (entity, demo_key))""")

        def record(entity, key, fields):
            # entity/column names come only from this file, never from user input.
            previous = connection.execute(
                "SELECT record_id FROM demo_seed_records WHERE entity=? AND demo_key=?",
                (entity, key)).fetchone()
            if previous and connection.execute(
                    f"SELECT id FROM {entity} WHERE id=?", (previous[0],)).fetchone():
                return previous[0]
            if entity == "users":
                existing = connection.execute("SELECT id FROM users WHERE email=?", (fields["email"],)).fetchone()
                if existing:
                    # Do not take ownership of or alter an existing account.
                    raise ValueError(f"Demo email already exists outside this seed: {fields['email']}")
            columns = ", ".join(fields)
            placeholders = ", ".join("?" for _ in fields)
            result = connection.execute(
                f"INSERT INTO {entity} ({columns}) VALUES ({placeholders})", tuple(fields.values()))
            connection.execute("INSERT OR REPLACE INTO demo_seed_records VALUES (?, ?, ?)",
                               (entity, key, result.lastrowid))
            inserted[entity] += 1
            return result.lastrowid

        users = []
        record("users", "admin", dict(name="Demo Store Admin", email="admin@demo.example",
               password=DEMO_PASSWORD, is_admin=1, created_at="2026-10-01 08:00:00"))
        for index, name in enumerate(CUSTOMERS, 1):
            users.append(record("users", f"customer-{index}", dict(
                name=name, email=f"customer{index}@demo.example", password=DEMO_PASSWORD,
                is_admin=0, created_at=f"2026-10-01 09:{index:02d}:00")))

        products = {}
        prices = {}
        for index, (key, title, category, price, stock, description) in enumerate(PRODUCTS):
            timestamp = (datetime(2026, 10, 2, 9) + timedelta(hours=index)).strftime("%Y-%m-%d %H:%M:%S")
            products[key] = record("products", key, dict(title=title, category=category,
                price=float(price), stock=stock, description=description,
                image_url="", created_at=timestamp, updated_at=timestamp))
            prices[key] = Decimal(price)

        for index, items in enumerate(ORDER_ITEMS):
            timestamp = (datetime(2026, 10, 3, 10) + timedelta(hours=index * 12)).strftime("%Y-%m-%d %H:%M:%S")
            total = sum((prices[key] * quantity for key, quantity in items), Decimal("0.00"))
            order_id = record("orders", f"order-{index+1}", dict(user_id=users[index % len(users)],
                total=float(total), status=STATUSES[index], created_at=timestamp, updated_at=timestamp))
            for line, (key, quantity) in enumerate(items, 1):
                record("order_items", f"order-{index+1}-line-{line}", dict(
                    order_id=order_id, product_id=products[key], quantity=quantity, price=float(prices[key])))

        comments = ["Comfortable and easy to use.", "Great quality for a home office.",
                    "Arrived as described; useful every day.", "A practical addition to my routine."]
        for index, (key, *_rest) in enumerate(PRODUCTS[:10]):
            record("reviews", f"review-{index+1}", dict(product_id=products[key],
                user_id=users[index % len(users)], rating=[5, 4, 5, 4, 3][index % 5],
                comment=comments[index % 4], created_at="2026-10-10 14:00:00"))

        if connection.execute("PRAGMA foreign_key_check").fetchall():
            raise ValueError("Foreign-key validation failed; no demo changes were saved.")
        invalid_totals = connection.execute("""SELECT o.id FROM orders o
            JOIN order_items i ON i.order_id=o.id GROUP BY o.id
            HAVING ABS(o.total - SUM(i.quantity * i.price)) > 0.005""").fetchall()
        if invalid_totals:
            raise ValueError("Order totals do not match their line items; rolling back.")
        connection.commit()
        summary = {
            "dataset": "eCommerce AI synthetic demo v1",
            "inserted": inserted,
            "demo_counts": dict(connection.execute(
                "SELECT entity, COUNT(*) FROM demo_seed_records GROUP BY entity").fetchall()),
            "demo_order_value": round(connection.execute("""SELECT SUM(o.total) FROM orders o
                JOIN demo_seed_records d ON d.entity='orders' AND d.record_id=o.id""").fetchone()[0], 2),
            "demo_admin": "admin@demo.example",
            "demo_password": DEMO_PASSWORD,
            "database": DATABASE.relative_to(ROOT).as_posix(),
        }
        summary_path = ROOT / "docs" / "demo-data-summary.json"
        summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(summary, indent=2))
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


if __name__ == "__main__":
    seed()
