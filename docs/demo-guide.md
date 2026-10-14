# eCommerce AI demo guide

Updated: 11 October 2026. All demo people, orders and reviews are fictional.

## Problem and solution

Store operators need one place to inspect their catalog, stock and orders, and
to understand how demand or scarce inventory might affect a price. An empty
prototype cannot demonstrate these workflows or meaningful dashboard totals.

The current solution combines a React admin interface, an Express REST API and
a local SQLite database. The seeded data makes the existing catalog, product
management, order inspection, dashboard and pricing sandbox usable for a local
demonstration. It is a prototype; the capabilities below describe the running
Node/SQLite variant, rather than every feature proposed in the original README.

## Run and populate

From the project directory, start the existing backend in PowerShell:

```powershell
Set-Location backend-mern
$env:PORT = '6220'
node server.js
```

It serves the React production build and `/api/*` on the same port. Visit
<http://localhost:6220/dashboard>. For a fresh clone, install both Node packages and build the frontend using

```sh
npm ci --prefix backend-mern
npm ci --prefix frontend-react
npm run build --prefix frontend-react
npm run init-db --prefix backend-mern
```

The standalone build uses the package's own dependency versions; no workspace
ESLint override is required. See the root README for combined-server and React
development-server port settings.

From the project directory, add the synthetic dataset:

```powershell
python tools/seed_demo_data.py
```

The seed uses only Python's standard library. It validates the app schema,
backs up the database before the first run, inserts records in a transaction,
and records their IDs in `demo_seed_records`. Repeated runs add no duplicates
and preserve existing records. Existing rows edited in the UI are not reset.
The initial backup is `tmp/demo-data/ecommerce-before-demo.sqlite`.
The machine-readable dataset summary is `docs/demo-data-summary.json`.

## Dataset

| Entity | Demo count | Purpose |
|--------|------------|---------|
| Products | 12 | Six categories; normal, low and zero stock examples |
| Accounts | 9 | One admin and eight fictional customers |
| Orders | 16 | Eight delivered, four shipped, two processing, two pending |
| Order items | 36 | Quantity and unit-price calculations linked to products |
| Reviews | 10 | Stored sample records; no review screen in this React app |

The demo orders total **$2,047.50**, averaging **$127.97**. Prices follow the
USD display already used by the frontend. This is sample order value, not
verified payments or recognized sales. Stock is an illustrative current
snapshot and is not decremented automatically by the order API.

Demo account: `admin@demo.example` / `DemoStore2026!`. Customer addresses use
the same `.example` domain. These are public demo credentials. The current UI
sign-in simply navigates to the dashboard; it does not validate them through
the login API. The backend login endpoint can validate the stored demo account.

## Walkthrough

1. **Dashboard:** confirm 12 products, 16 orders and $2,047.50 in gross order value.
2. **Catalog:** browse Electronics, Office, Home & Kitchen, Fitness, Lifestyle
   and Accessories. `Pulse Smartwatch` has stock 3; `Connect USB-C Hub` has stock 0.
3. **Orders:** inspect order #16: smartwatch $129, backpack $54 and organizer
   $22, totaling $205. IDs may differ if data existed before seeding.
4. **AI studio:** choose `Pulse Smartwatch`, set demand factor to `0.8` and
   competitor price to `145`, and click **Run pricing**. The result is **$154.80**.

Pricing uses a deterministic rule:

```text
129 * (1 + 0.2 * 0.8) = 149.64
149.64 * 1.1 = 164.604             # stock below 5
(164.604 + 145) / 2 = 154.802      # blend with lower competitor price
round to cents = 154.80
```

The sandbox previews a price; it does not change the catalog's stored price.

## Implemented scope and boundaries

- Product listing and CRUD, order creation and inspection, registration and a
  basic login API, and SQLite persistence are implemented in the Node backend.
- The React UI provides dashboard, catalog, product management, orders, pricing
  and theme settings. The order screen inspects records; it does not implement
  fulfillment status updates or a customer checkout.
- The recommendation endpoint selects the newest products. It is not a trained
  or personalized recommender, and does not filter out zero-stock items.
- The pricing endpoint uses demand, current stock and competitor-price inputs.
- Conversion rate `3.4%`, inventory coverage `98%`, and the marketplace pulse
  chart are display placeholders. Counts, average order value and total order
  value are derived from the API data on page load.
- The Python shared AI modules and the FastAPI/Django alternatives remain
  separate examples. They are not running or connected to this Node demo.
- Passwords are currently stored in plaintext and routes lack authorization.
  Sessions, password hashing and role enforcement remain implementation work.
- Payments, shipping integration, a customer cart/checkout, production analytics
  and integrated vector search/forecasting are outside the demonstrated scope.

## Changes and validation

The missing `sqlite3` native binding was rebuilt to allow startup. The Node
server runs on port 6220 and serves both UI and API. This update adds the
repeatable dataset and fixes light-mode contrast for catalog names, values and
labels. The React production build was regenerated for the contrast fix.

Validation covers SQLite integrity, foreign-key consistency, order totals, a
second seed run with zero insertions, dashboard/catalog/order rendering, and
the pricing result. Screenshots in `docs/assets` were captured from the local
app. The three-page PDF is `output/pdf/E-Commerce-Project-Overview.pdf`.

To regenerate the brief after replacing its screenshots, run
`python docs/generate_demo_pdf.py` with ReportLab installed.

Implementation evidence: `backend-mern/server.js`, `backend-mern/db.js`,
`backend-mern/routes/orderRoutes.js`, `backend-mern/controllers/aiController.js`,
`backend-mern/controllers/authController.js`, and the corresponding components
in `frontend-react/src`.
