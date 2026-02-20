📊 Sales ETL Pipeline with Apache Airflow

An end-to-end data engineering pipeline that extracts product data from an external API, stores raw data, transforms it into an analytics-ready structure, and loads it into a PostgreSQL (Supabase) staging table — orchestrated using Apache Airflow and fully containerized with Docker.

🚀 Project Overview

This project simulates a production-style ETL workflow:

Extract – Retrieve product data from FakeStore API
Load (Raw) – Persist raw JSON data
Transform – Clean, flatten, and enrich data
Load (Staging) – Upsert into PostgreSQL (Supabase)
Orchestration – Managed via Apache Airflow
Infrastructure – Dockerized services

🏗 Architecture
FakeStore API
     ↓
Airflow DAG
     ↓
Raw Data Storage (JSON)
     ↓
Transformation Layer
     ↓
Supabase (PostgreSQL - Staging)

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


│   └── logger.py
│
├── requirements.txt
├── .env
└── README.md
⚙️ Key Features

✔ API data ingestion
✔ Raw data persistence
✔ Data transformation & enrichment
✔ PostgreSQL staging layer
✔ Idempotent loads (Upserts)
✔ Airflow orchestration
✔ Dockerized environment

🔄 Pipeline Workflow
1️⃣ Extraction

Calls FakeStore API

Retrieves product data (JSON)

Stores raw dataset

Passes file path to downstream tasks

2️⃣ Transformation

Flattens nested fields (e.g., ratings)

Standardizes schema

Adds metadata columns:

ingestion_date

loaded_at

3️⃣ Load to Staging

Ensures table exists

Performs bulk insert

Uses ON CONFLICT for safe upserts

🐳 Running the Project
1️⃣ Start Services
docker compose up --build
2️⃣ Access Airflow UI

Open in browser:

http://localhost:8080

Default credentials:

Username: airflow
Password: airflow
3️⃣ Trigger the DAG

DAG Name:

sales_pipeline_raw_ingestion

Click ▶ Trigger

🗄 Database (Supabase / PostgreSQL)

Data is loaded into:

products_staging
Schema

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

Sensitive credentials are stored in .env:

POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
DB_URL=
📈 Production Concepts Demonstrated

✅ Data Lake (Raw Layer)
✅ Staging Layer
✅ Idempotent Loads
✅ Schema-on-write
✅ Metadata Tracking
✅ Workflow Orchestration
✅ Containerized Infrastructure

🎯 Learning Objectives

This project was built to strengthen skills in:

Apache Airflow DAG design
Dockerized data pipelines
API ingestion patterns
Data transformation
PostgreSQL loading
Production ETL best practices

🚧 Future Enhancements

⬜ Data quality checks
⬜ Data warehouse layer
⬜ Incremental loading strategy
⬜ Partitioning & indexing
⬜ Monitoring & alerting
⬜ CI/CD pipeline

👨‍💻 Author

Samwel Ngugi
Junior Data Engineer

Focused on designing and building production-grade data pipelines
