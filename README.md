# Product Importer – Backend Assignment

A scalable FastAPI-based web application for importing, managing, and processing large product datasets (up to ~500,000 records) from CSV files. The system is designed to handle long-running jobs asynchronously, provide real-time progress feedback, and support webhook notifications — closely simulating real-world backend data-flow systems.

---

## Project Structure

```
product-importer/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── db.py
│   ├── models.py
│   ├── schemas.py
│   ├── celery_worker.py
│   ├── config.py
│   │
│   ├── api/
│   │   ├── products.py
│   │   ├── upload.py
│   │   ├── jobs.py
│   │   └── webhooks.py
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   └── static/
│       └── app.js
│
├── requirements.txt
├── Dockerfile
├── README.md
```

---

## Core Features

### 1. CSV Product Import (Asynchronous)

* Upload CSV files containing up to **500,000 product records**
* File upload via web UI
* Background processing using **Celery**
* SKU is treated as **case-insensitive unique**
* Existing products are overwritten on SKU conflict
* Import progress tracked and exposed via API

### 2. Real-Time Job Progress

* Job lifecycle: `pending → processing → completed / failed`
* Progress data includes:

  * Total records
  * Processed records
  * Current status
* Frontend displays live progress using polling or Server-Sent Events (SSE)

### 3. Product Management UI

* View products with pagination
* Create, update, delete individual products
* Filter by SKU, name, active status, description
* Bulk delete all products with confirmation

### 4. Webhook Management

* Configure multiple webhook endpoints
* Enable / disable webhooks
* Test webhook delivery from UI
* Webhooks are fired asynchronously via Celery
* Captures response status and latency

### 5. Production-Ready Architecture

* FastAPI for API layer
* SQLAlchemy ORM with PostgreSQL
* Celery + Redis for async jobs
* Clean dependency injection
* Dockerized for deployment

---

## File Responsibilities

### `app/main.py`

* FastAPI application entry point
* Registers routers
* Initializes database tables
* Serves HTML UI

### `app/database.py`

* Defines SQLAlchemy engine
* Creates session factory (`SessionLocal`)
* Declares ORM base (`Base`)
* Contains **no business logic**

### `app/db.py`

* Centralized database session dependency
* Provides `get_db()` for FastAPI routes
* Ensures consistent session lifecycle

### `app/models.py`

* SQLAlchemy ORM models
* Defines Product, ImportJob, Webhook schemas
* Enforces database-level constraints (e.g., unique SKU)

### `app/schemas.py`

* Pydantic schemas for request/response validation
* Separates API contracts from ORM models

### `app/celery_worker.py`

* Celery app configuration
* Registers background tasks:

  * CSV import processing
  * Webhook firing

### `app/config.py`

* Centralized configuration
* Environment variable management
* Database and Redis URLs

### `app/api/products.py`

* CRUD APIs for products
* Pagination and filtering
* Bulk delete with confirmation flag

### `app/api/upload.py`

* CSV file upload endpoint
* Creates import job record
* Dispatches Celery task

### `app/api/jobs.py`

* Job status endpoints
* Progress polling
* Optional SSE endpoint for real-time updates

### `app/api/webhooks.py`

* Webhook CRUD operations
* Test webhook endpoint
* Triggers asynchronous webhook delivery

### `app/templates/index.html`

* Minimal UI for:

  * File upload
  * Job progress display
  * Product management
  * Webhook configuration

### `app/static/app.js`

* Frontend JavaScript
* Handles:

  * File upload
  * Polling / SSE for job progress
  * UI updates

---

## Running the Application (Local)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start Redis

```bash
redis-server
```

### 3. Run Celery Worker

```bash
celery -A app.celery_worker.celery worker --loglevel=info
```

### 4. Run FastAPI App

```bash
uvicorn app.main:app --reload
```

### 5. Open UI

```
http://localhost:8000
```

---

## Environment Variables

```
DATABASE_URL=postgresql://user:password@localhost:5432/products
REDIS_URL=redis://localhost:6379/0
```

---

## Deployment

* Fully Docker-compatible
* Designed to run on:

  * Render
  * Heroku
  * AWS / GCP
* Long-running tasks handled asynchronously to avoid platform timeouts

---

## Design Principles

* Single source of truth for DB sessions
* No blocking operations in request handlers
* Explicit separation of concerns
* Readable, maintainable, reviewer-friendly codebase

---

## Notes for Reviewers

This project intentionally mirrors real-world backend challenges:

* Large dataset ingestion
* Background job orchestration
* Progress reporting
* Webhook delivery guarantees

The code prioritizes **clarity, correctness, and scalability** over shortcuts.
