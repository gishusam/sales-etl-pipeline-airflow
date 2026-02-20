import json
import psycopg2
import os
from supabase import create_client
from psycopg2.extras import execute_values
from datetime import datetime
from typing import List, Dict
from airflow.models import Variable
from utils.logger import logger


TABLE_NAME = "products_staging"


TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS products_staging (
    id INTEGER PRIMARY KEY,
    title TEXT,
    price NUMERIC,
    description TEXT,
    category TEXT,
    image TEXT,
    rating_rate NUMERIC,
    rating_count INTEGER,
    ingestion_date DATE,
    loaded_at TIMESTAMP
);
"""


def ensure_table_exists(cursor):
    cursor.execute(TABLE_SCHEMA)


def download_from_supabase(supabase_uri: str) -> str:
    """
    Downloads file from Supabase Storage to local disk.
    Returns local file path.
    """

    logger.info(f"Downloading file from Supabase: {supabase_uri}")

    project_url = Variable.get("SUPABASE_URL")
    service_key = Variable.get("SUPABASE_SERVICE_KEY")

    supabase = create_client(project_url, service_key)

    # Remove supabase:// prefix
    clean_uri = supabase_uri.replace("supabase://", "")

    
    bucket, file_path = clean_uri.split("/", 1)

    
    logger.info(f"Bucket: {bucket}")
    logger.info(f"File path: {file_path}")

    # Download file (returns bytes)
    file_bytes = supabase.storage.from_(bucket).download(file_path)

    # ✅ Absolute path (Airflow/Docker safe)
    local_dir = "/opt/airflow/data/raw"
    local_path = os.path.join(local_dir, file_path)

    # Preserve folder structure
    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    with open(local_path, "wb") as f:
        f.write(file_bytes)

    logger.info(f"File downloaded to: {local_path}")

    return local_path


def transform_products(raw_products: List[Dict]) -> List[Dict]:
    """
    Transform raw API JSON into flat structure for staging.
    """

    transformed = []
    ingestion_date = datetime.utcnow().date()
    loaded_at = datetime.utcnow()

    for product in raw_products:
        transformed.append({
            "id": product["id"],
            "title": product["title"],
            "price": product["price"],
            "description": product["description"],
            "category": product["category"],
            "image": product["image"],
            "rating_rate": product.get("rating", {}).get("rate"),
            "rating_count": product.get("rating", {}).get("count"),
            "ingestion_date": ingestion_date,
            "loaded_at": loaded_at
        })

    return transformed


def load_to_staging(transformed_data: List[Dict]):

    if not transformed_data:
        logger.warning("No transformed data to load.")
        return

    columns = transformed_data[0].keys()

    insert_query = f"""
        INSERT INTO {TABLE_NAME} ({', '.join(columns)})
        VALUES %s
        ON CONFLICT (id) DO UPDATE SET
        {', '.join([f"{col}=EXCLUDED.{col}" for col in columns if col != "id"])};
    """

    values = [
        tuple(item[col] for col in columns)
        for item in transformed_data
    ]

    db_url = Variable.get("DB_URL")
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()

    try:
        ensure_table_exists(cursor)
        execute_values(cursor, insert_query, values)
        conn.commit()
        logger.info(f"Loaded {len(values)} records into {TABLE_NAME}")

    except Exception as e:
        conn.rollback()
        logger.error(f"Staging load failed: {e}")
        raise

    finally:
        cursor.close()
        conn.close()


def transform_and_load(raw_file_path: str):
    """
    Entry point for Airflow.
    Reads RAW JSON → transforms → loads STAGING.
    """

    logger.info(f"Original raw_file_path repr: {repr(raw_file_path)}")

    raw_file_path = raw_file_path.strip()

    # ✅ Detect Supabase URI
    if raw_file_path.startswith("supabase://"):
        logger.info("Supabase path detected. Initiating download...")
        raw_file_path = download_from_supabase(raw_file_path)

    logger.info(f"Reading raw data from: {raw_file_path}")

    with open(raw_file_path, "r") as f:
        raw_products = json.load(f)

    transformed = transform_products(raw_products)
    load_to_staging(transformed)
