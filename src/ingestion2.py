import logging
from pathlib import Path
import boto3



logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
s3_client = boto3.client("s3")

bucket_name = "michael-olx-data-lake"

files = {
    "olist_customers_dataset.csv": "bronze/customers/",
    "olist_geolocation_dataset.csv": "bronze/geolocation/",
    "olist_order_items_dataset.csv": "bronze/order_items/",
    "olist_order_payments_dataset.csv": "bronze/order_payments/",
    "olist_order_reviews_dataset.csv": "bronze/order_reviews/",
    "olist_orders_dataset.csv": "bronze/orders/",
    "olist_products_dataset.csv": "bronze/products/",
    "olist_sellers_dataset.csv": "bronze/sellers/",
    "product_category_name_translation.csv": "bronze/product_category/"
}



# Locates the project root directory relative to this file: src/ -> project root -> data/
DATASET_FOLDER = Path(__file__).resolve().parent.parent / "data"

for file_name, destination in files.items():
    local_file = DATASET_FOLDER / file_name

    if not local_file.exists():
        logging.warning(f"{file_name} not found at {local_file}")
        continue

    s3_key = f"{destination}{file_name}"

    logging.info(f"Uploading {file_name}...")

    s3_client.upload_file(
        str(local_file),
        bucket_name,
        s3_key
    )

    logging.info(f"Uploaded to s3://{bucket_name}/{s3_key}")