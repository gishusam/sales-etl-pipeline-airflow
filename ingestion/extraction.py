import json
import requests
from supabase import create_client
from utils.logger import logger
from airflow.models import Variable



def extract_data(api_url: str, execution_date: str) -> str:
    """
    Extracts data from API and uploads raw JSON to Supabase Storage.
    Returns the Supabase storage path.
    """

    logger.info("Starting API extraction")

    # --- API call ---
    response = requests.get(
        api_url,
        timeout=30
    )
    response.raise_for_status()

    data = response.json()

    if not data:
        raise ValueError("API returned empty payload")

    logger.info(f"Extracted {len(data)} records")

    # --- Supabase client ---
    supabase = create_client(
        Variable.get("SUPABASE_URL"),
        Variable.get("SUPABASE_SERVICE_KEY")
    )
    bucket = Variable.get("SUPABASE_RAW_BUCKET")
    object_path = (
        f"raw/api_name/"
        f"ingestion_date={execution_date}/"
        f"data.json"
    )

    payload = json.dumps(data).encode("utf-8")

    # --- Upload ---
    try:
        supabase.storage.from_(bucket).upload(
            path=object_path,
            file=payload,
            file_options={
                "content-type": "application/json",
                "x-upsert": "true"
            }
        )
    except Exception as e:
        raise RuntimeError(f"Supabase upload failed: {e}")

    logger.info(f"Raw data uploaded to supabase://{bucket}/{object_path}")

    return f"supabase://{bucket}/{object_path}"