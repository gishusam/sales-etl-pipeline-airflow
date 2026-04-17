# Sales ETL Pipeline

A production-grade ELT pipeline that ingests product catalogue data from a REST API, applies schema enforcement and transformation logic, and loads into a PostgreSQL staging warehouse — orchestrated with Apache Airflow and containerised with Docker.

The focus of this project is **pipeline architecture and engineering patterns**, not the data source: idempotent ingestion, decoupled module design, structured logging, UPSERT loading, and date-partitioned paths that support backfill without data duplication.

---

## The Problem

Retail and e-commerce data teams regularly ingest product catalogue feeds from vendor APIs — pricing, inventory, ratings — into internal warehouses for downstream analytics. These feeds arrive in raw JSON, are inconsistently typed, and need to be loaded reliably and repeatedly without creating duplicates or requiring full table refreshes.

This pipeline solves the core engineering challenge: ingest reliably, transform consistently, and load idempotently — with a DAG that can be triggered daily or backfilled for any historical date range.

---

## Architecture

```
REST API (Product Catalogue Feed)
          │
          ▼
  Extraction Layer (Python)
  extraction.py — fetches JSON, validates response
          │
          ▼
  Transformation Layer (Python)
  transformation.py — flattens nested fields, enforces schema,
                       casts types, adds ingestion metadata
          │
          ▼
  PostgreSQL (Staging Layer)
  products_staging — UPSERT on primary key, idempotent
          │
          ▼
  Apache Airflow DAG
  sales_ingestion_dag.py — orchestrates full pipeline,
                            date-partitioned, backfill-safe
```

**Key design decisions:**
- Extraction and transformation modules are fully decoupled from Airflow — they can be tested and run independently without a running scheduler
- UPSERT logic (`ON CONFLICT DO UPDATE`) means re-running the pipeline for the same date never creates duplicates
- `ingestion_date` field on every row enables date-partition filtering for incremental downstream consumption
- Structured logging at every stage makes debugging straightforward in both local and containerised environments

---

## Tech Stack

| Layer | Tool |
|---|---|
| Ingestion | Python, REST API |
| Transformation | Python (type enforcement, schema normalisation) |
| Storage | PostgreSQL (Supabase) |
| Orchestration | Apache Airflow |
| Infrastructure | Docker, Docker Compose |
| Logging | Python logging (structured, centralised) |

---

## Repository Structure

```
sales-etl-pipeline/
├── airflow/
│   └── dags/
│       └── sales_ingestion_dag.py    — Airflow DAG definition
├── ingestion/
│   ├── extraction.py                 — API fetch + response validation
│   └── transformation.py             — flatten, cast, enforce schema
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── utils/
│   └── logger.py                     — centralised structured logging
├── requirements.txt
├── .env.example
└── README.md
```

---

## Warehouse Schema

**Table:** `products_staging`

| Column | Type | Notes |
|---|---|---|
| `id` | INTEGER | Primary key — UPSERT target |
| `title` | TEXT | Product name |
| `price` | NUMERIC | Cast from raw string |
| `description` | TEXT | |
| `category` | TEXT | |
| `image` | TEXT | URL |
| `rating_rate` | NUMERIC | Flattened from nested `rating.rate` |
| `rating_count` | INTEGER | Flattened from nested `rating.count` |
| `ingestion_date` | DATE | Pipeline run date — partition key |
| `loaded_at` | TIMESTAMP | Row-level load timestamp |

`rating_rate` and `rating_count` are flattened from a nested JSON object in the raw feed — a common transformation pattern when ingesting vendor API responses that embed sub-objects.

---

## Setup & Running

**Prerequisites:** Docker, Docker Compose

```bash
# 1. Clone the repo
git clone https://github.com/gishusam/sales-etl-pipeline.git
cd sales-etl-pipeline

# 2. Configure environment
cp .env.example .env
# Edit .env with your PostgreSQL credentials

# 3. Start the full stack (Airflow + PostgreSQL)
docker compose up --build

# 4. Access Airflow UI
# http://localhost:8080  (airflow / airflow)
# Trigger DAG: sales_pipeline_raw_ingestion

# 5. Verify load
# psql into your DB and run:
# SELECT COUNT(*), ingestion_date FROM products_staging GROUP BY 2;
```

**Running without Airflow (local test):**
```bash
pip install -r requirements.txt
python main.py
```

**Expected output:**
```
INFO - ===== ETL Pipeline Started =====
INFO - Successfully extracted 20 records
INFO - Transformation completed — 20 records, 0 nulls in primary key
INFO - Connected to database successfully
INFO - Table 'products_staging' ready
INFO - Loaded 20 records via UPSERT
INFO - ===== ETL Pipeline Completed Successfully =====
```

---

## Engineering Patterns Demonstrated

**Idempotent ingestion** — running the pipeline twice for the same date produces the same result, never duplicates. Achieved via `INSERT ... ON CONFLICT (id) DO UPDATE`.

**Decoupled modules** — `extraction.py` and `transformation.py` have no Airflow dependency. They are plain Python functions that can be unit tested, imported, or swapped independently.

**Date-partitioned loading** — every row carries an `ingestion_date` field. This means downstream consumers can query `WHERE ingestion_date = '2025-01-15'` without full scans, and the pipeline supports backfilling any date range without side effects.

**Structured logging** — a centralised `logger.py` module applies consistent log formatting across all pipeline stages, making it straightforward to ship logs to a monitoring tool (Datadog, CloudWatch) with no refactoring.

---

## What I'd Build Next

- **dbt transformation layer** — add a mart model on top of staging for category-level aggregations and rating distribution analysis
- **Data quality tests** — assert non-null primary keys, price > 0, rating_rate between 0 and 5 on every run
- **Incremental Airflow DAG** — switch from full-refresh to `@daily` schedule with `execution_date` parameterisation for true incremental loading
- **GCP deployment** — move PostgreSQL to Cloud SQL, run Airflow on Cloud Composer, trigger via Cloud Scheduler

---

## Author

**Samwel Ngugi** — Data Engineer, Nairobi, Kenya (open to remote)

[GitHub](https://github.com/gishusam) · [LinkedIn](https://linkedin.com/in/samwelngugi) · [Kenya Economic Intelligence Pipeline](https://kenya-economic-intelligence.streamlit.app)
