import logging
from pathlib import Path

import boto3
import pandas as pd


# -----------------------------
# Configuration
# -----------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

BUCKET_NAME = "cloudlake-34081b81"

DATASET_FOLDER = Path("data")
SILVER_FOLDER = Path("silver_data")

files = [
    "olist_customers_dataset.csv",
    "olist_geolocation_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_orders_dataset.csv",
    "olist_products_dataset.csv",
    "olist_sellers_dataset.csv",
    "product_category_name_translation.csv",
]

# Map each dataset to its own Silver S3 folder
silver_prefixes = {
    "olist_customers_dataset.csv": "customers",
    "olist_geolocation_dataset.csv": "geolocation",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "order_payments",
    "olist_order_reviews_dataset.csv": "order_reviews",
    "olist_orders_dataset.csv": "orders",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
    "product_category_name_translation.csv": "product_category",
}

s3 = boto3.client("s3")


# -----------------------------
# Helper functions
# -----------------------------

def standardize_columns(df):
    """Standardize dataframe column names."""

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    return df


def convert_datetime_columns(df):
    """Convert columns containing date/time values."""

    for column in df.columns:

        if "date" in column or "timestamp" in column:

            try:
                df[column] = pd.to_datetime(
                    df[column],
                    errors="coerce"
                )

            except Exception as error:
                logging.warning(
                    f"Could not convert {column}: {error}"
                )

    return df


# -----------------------------
# Transformation
# -----------------------------

SILVER_FOLDER.mkdir(exist_ok=True)

for file_name in files:

    input_file = DATASET_FOLDER / file_name

    if not input_file.exists():
        logging.warning(
            f"{file_name} not found. Skipping."
        )
        continue

    logging.info(f"Processing {file_name}")

    df = pd.read_csv(input_file)

    original_rows = len(df)

    # Standardize column names
    df = standardize_columns(df)

    # Remove exact duplicate rows
    df = df.drop_duplicates()

    # Convert date/time columns
    df = convert_datetime_columns(df)

    # Create Parquet filename
    parquet_name = file_name.replace(
        ".csv",
        ".parquet"
    )

    output_file = SILVER_FOLDER / parquet_name

    # Write Parquet
    df.to_parquet(
        output_file,
        index=False
    )

    logging.info(
        f"{file_name}: "
        f"{original_rows} rows → {len(df)} rows"
    )

    logging.info(
        f"Saved Silver file: {output_file}"
    )


# -----------------------------
# Upload Silver data to S3
# -----------------------------

for file_name in files:

    parquet_name = file_name.replace(
        ".csv",
        ".parquet"
    )

    local_file = SILVER_FOLDER / parquet_name

    if not local_file.exists():
        logging.warning(
            f"{parquet_name} not found. Skipping upload."
        )
        continue

    dataset_folder = silver_prefixes[file_name]

    # Create dataset-specific S3 prefix
    s3_key = (
        f"silver/"
        f"{dataset_folder}/"
        f"{parquet_name}"
    )

    logging.info(
        f"Uploading {parquet_name} to S3"
    )

    s3.upload_file(
        str(local_file),
        BUCKET_NAME,
        s3_key
    )

    logging.info(
        f"Uploaded to "
        f"s3://{BUCKET_NAME}/{s3_key}"
    )


print(
    "Silver transformation and upload completed successfully."
)