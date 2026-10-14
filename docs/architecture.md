# Architecture

The demonstrated application is React → Express REST API → SQLite. `backend-mern/server.js` serves the React build and mounts product, user, order and pricing/recommendation routes. `backend-mern/db.js` initializes the relational schema and exports parameterized query helpers. `tools/seed_demo_data.py` populates repeatable fictional records.

## Data and workflows

Products carry price and stock. Orders reference users; line items reference orders and products. The order API writes a transaction and returns linked item descriptions. The UI reads dashboard totals from these APIs. Reviews are stored but have no review screen.

The JavaScript pricing controller adjusts the base price using demand, a low-stock premium and a competitor blend. The recommendation endpoint returns recent products. Neither endpoint invokes the Python examples.

## Separate examples

`shared/` contains a SentenceTransformers embedding wrapper, vector similarity search/recommendation, moving-average forecasting, rule-based pricing and placeholder sentiment logic. FastAPI and Django show alternatives. They require their own dependency/configuration work and have not been validated as replacements for the active Node API.

Old Mongoose model/config files are dormant; the running server uses SQLite. The frontend does not contain shopping-cart/product-detail modules described in earlier plans.

## Boundaries

Local demonstration authentication is incomplete. Persistent orders are not a checkout/payment integration, and displayed order value is not payment revenue. See the root README and demo guide for implemented scope.
