
🛒 Sales ETL Pipeline (API → PostgreSQL)

A production-style ETL (Extract, Transform, Load) pipeline that ingests product data from a public REST API, applies schema enforcement and transformations, and loads the data into a PostgreSQL staging table.

This project is designed as a portfolio-ready Data Engineering project, demonstrating modular architecture, structured logging, idempotent database operations, and workflow orchestration.

 📡 Data Source
- Public REST API: [FakeStore API](https://fakestoreapi.com/products)

🔄 Pipeline Stages

| Stage      | Description |
|------------|-------------|
| Extract    | Fetch raw JSON data from the API |
| Transform  | Clean, flatten, and enforce schema consistency |
| Load       | Create tables if needed and upsert into PostgreSQL |



## 🧱 Architecture

```text
FakeStore API
     ↓
Extraction Layer (Python)
     ↓
Raw Data (JSON)
     ↓
Transformation Layer
     ↓
PostgreSQL (Supabase - Staging)
````

---

## 📂 Project Structure

```text
sales-etl-pipeline/
│
├── airflow/ 🛠️
│   └── dags/
│       └── sales_ingestion_dag.py     # Airflow DAG for pipeline orchestration
│
├── ingestion/ 🔄
│   ├── extraction.py                   # Extract data from API
│   └── transformation.py               # Transform and clean data
│
├── docker/ 🐳
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── data/ 📦
│   └── raw/                            # Raw JSON files (optional)
│
├── utils/ ⚙️
│   └── logger.py                        # Centralized logging
│
├── requirements.txt                     # Python dependencies
├── .env                                 # Environment variables
└── README.md                            # Project documentation
```

---

## 🧠 Key Features

* Modular ETL design (Extract / Transform / Load)
* Apache Airflow orchestration
* Centralized structured logging
* Schema enforcement and data typing
* Idempotent table creation
* Bulk inserts with UPSERT logic
* Dockerized environment

---

## 🗄️ Database Schema

**Table:** products_staging

| Column         | Type      | Description              |
| -------------- | --------- | ------------------------ |
| id             | INTEGER   | Product ID (Primary Key) |
| title          | TEXT      | Product name             |
| price          | NUMERIC   | Product price            |
| description    | TEXT      | Product description      |
| category       | TEXT      | Product category         |
| image          | TEXT      | Product image URL        |
| rating_rate    | NUMERIC   | Average rating           |
| rating_count   | INTEGER   | Number of ratings        |
| ingestion_date | DATE      | Pipeline ingestion date  |
| loaded_at      | TIMESTAMP | Load timestamp           |

---

## ⚙️ Setup & Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/sales-etl-pipeline.git
cd sales-etl-pipeline
```

### 2️⃣ Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a .env file:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=sales_etl
DB_URL=postgresql://postgres:your_password@localhost:5432/sales_etl
```

---

## 🐳 Running with Docker (Recommended)

```bash
docker compose up --build
```

Access Airflow UI: [http://localhost:8080](http://localhost:8080)
Default credentials: airflow / airflow

Trigger DAG: sales_pipeline_raw_ingestion and click Trigger

---

## ▶️ Running Locally (Without Airflow)

```bash
python main.py
```

---

## ✅ Expected Output

```text
INFO - ===== ETL Pipeline Started =====
INFO - Successfully extracted 20 records
INFO - Transformation completed
INFO - Connected to database successfully
INFO - Table 'products_staging' is ready
INFO - Loaded 20 records
INFO - ===== ETL Pipeline Completed Successfully =====
```

---

## 🔍 Verifying the Data

```sql
SELECT COUNT(*) FROM products_staging;
SELECT * FROM products_staging LIMIT 5;
```

---

## 🧪 Possible Enhancements

* Incremental loading strategy
* Data quality checks
* Unit and integration tests
* Data warehouse layer
* Monitoring and alerts
* Cloud deployment (GCP / AWS / Azure)

---

## 🎯 Why This Project Matters

This project demonstrates:

* Real-world ETL architecture
* Production-style PostgreSQL loading
* Data transformation and schema enforcement
* Airflow orchestration
* Containerized data stack

It reflects practical skills used by Data Engineers in production environments.

---

## 👤 Author

Samwel Ngugi – Junior Data Engineer
Python | SQL | Airflow | ETL | Docker

If you found this project interesting, feel free to star the repository!


