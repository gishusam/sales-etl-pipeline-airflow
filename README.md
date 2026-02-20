📊 Sales ETL Pipeline with Airflow

An end-to-end data engineering pipeline that extracts product data from an API, stores raw data in cloud storage, transforms it, and loads it into a PostgreSQL (Supabase) staging table using Apache Airflow, Docker, and Python.

🚀 Project Overview

This project demonstrates a modern production-style ETL pipeline:

Extract – Pull product data from FakeStore API

Load (Raw) – Store raw JSON data

Transform – Clean & flatten nested fields

Load (Staging) – Upsert into PostgreSQL (Supabase)

Orchestration – Managed via Apache Airflow

Containerization – Fully Dockerized

🏗 Architecture

API → Airflow DAG → Raw Storage → Transformation → Supabase (Postgres)

🧰 Tech Stack

Python

Apache Airflow

Docker & Docker Compose

PostgreSQL (Supabase)

FakeStore API

psycopg2

Requests

📂 Project Structure
sales-etl-pipeline/
│
├── airflow/
│   └── dags/
│       └── sales_ingestion_dag.py
│
├── ingestion/
│   ├── extraction.py
│   └── transformation.py
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── data/
│   └── raw/
│
├── utils/
│   └── logger.py
│
├── requirements.txt
├── .env
└── README.md
⚙️ Features

✔ API data ingestion
✔ Raw data persistence
✔ Schema-on-write staging layer
✔ Idempotent loads (ON CONFLICT upsert)
✔ Airflow orchestration
✔ Dockerized environment

🔄 Pipeline Workflow
1️⃣ Extraction

Calls FakeStore API

Saves raw JSON file

Returns file path to Airflow

2️⃣ Transformation

Flattens nested rating fields

Adds metadata:

ingestion_date

loaded_at

3️⃣ Load to Staging

Ensures table exists

Bulk inserts using execute_values

Upserts on conflict

🐳 Running the Project
1️⃣ Start Services
docker compose up --build
2️⃣ Access Airflow UI

Open:

http://localhost:8080

Default credentials:

Username: airflow
Password: airflow
3️⃣ Trigger DAG

DAG Name:

sales_pipeline_raw_ingestion

Click ▶ Trigger

🗄 Database (Supabase)

Pipeline loads into:

products_staging

Schema includes:

id

title

price

description

category

image

rating_rate

rating_count

ingestion_date

loaded_at

🔐 Environment Variables

Sensitive configs stored in .env:

POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
DB_URL=
📈 Production Concepts Demonstrated

✅ Data Lake (Raw layer)
✅ Staging Layer
✅ Idempotent Loads
✅ Metadata Columns
✅ Orchestration
✅ Containerized Infra

🎯 Learning Objectives

This project was built to practice:

Airflow DAG design

Dockerized pipelines

API ingestion

Data transformation

PostgreSQL loading

Production ETL patterns

🚧 Future Improvements

⬜ Data quality checks
⬜ Warehouse layer
⬜ Incremental loads
⬜ Partitioning strategy
⬜ Monitoring & alerts
⬜ CI/CD pipeline

👨‍💻 Author

Samwel Ngugi

Aspiring Data Engineer
Focused on building production-grade data pipelines
