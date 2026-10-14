# CloudLake — AWS Data Lake Engineering Project

**CloudLake** is an end-to-end data engineering project that demonstrates how to build a cloud data lake using Terraform, Amazon S3, Python, AWS Glue, and Amazon Athena.

Using the Brazilian E-Commerce Public Dataset by Olist, the project ingests raw data, transforms it into cleaned Parquet datasets, catalogs the data, and models business-ready tables for downstream analytics.

## Project Architecture

```text
Olist E-Commerce Dataset
          |
          v
    Python Ingestion
          |
          v
     Amazon S3
     Bronze Layer
       (Raw CSV)
          |
          v
 Python Transformation
          |
          v
     Amazon S3
     Silver Layer
   (Cleaned Parquet)
          |
          v
       AWS Glue
  Crawler and Catalog
          |
          v
     Amazon Athena
          |
          v
      Gold Layer
 (Analytical Parquet Tables)
          |
          v
  Business Intelligence
    and Analytics
```

## Technology Stack

| Technology | Purpose |
|---|---|
| Terraform | Infrastructure provisioning and management |
| Amazon S3 | Cloud storage for Bronze, Silver, and Gold data |
| Python | Data ingestion and transformation |
| Pandas | Data cleaning and manipulation |
| Boto3 | AWS service interaction from Python |
| AWS Glue | Data discovery and cataloging |
| Amazon Athena | Serverless SQL analytics and Gold table creation |
| SQL | Data modeling and business aggregations |
| Git and GitHub | Version control and project collaboration |

## Dataset

The project uses the Brazilian E-Commerce Public Dataset by Olist, available on Kaggle.

Dataset: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

The project processes nine CSV datasets covering customers, geolocation, order items, payments, reviews, orders, products, sellers, and product category translations.

## Data Lake Design

### 1. Bronze Layer — Raw Data

Raw Olist CSV files are ingested into Amazon S3 using Python and Boto3.

 <img width="1365" height="597" alt="Screenshot 2026-10-14 201231" src="https://github.com/user-attachments/assets/090d6ef0-dbd3-484d-8cdb-2a1904896c10" />
This layer preserves the original source data for subsequent processing.

### 2. Silver Layer — Cleaned Data

Python and Pandas transform the raw datasets into Parquet format.

The transformation process includes:

- Standardizing column names.
- Removing exact duplicate rows.
- Converting applicable date and timestamp columns.
- Saving datasets in Parquet format.
- Organizing transformed datasets into separate S3 prefixes.
<img width="1366" height="595" alt="Screenshot 2026-10-14 201621" src="https://github.com/user-attachments/assets/af708432-7d0c-414b-bd8a-c5b475399cb6" />



This layer provides a consistent structure for querying and analytical processing.

### 3. Gold Layer — Business-Ready Data

Amazon Athena is used to model Silver datasets into four analytical tables. The resulting Parquet data is stored in Amazon S3.

The current Gold layer contains the following datasets:
<img width="1366" height="569" alt="Screenshot 2026-10-14 201751" src="https://github.com/user-attachments/assets/e67355ea-63ea-4b14-9c3f-1b3a689487ba" />

| S3 folder | Business purpose |
|---|---|
| `customer_orders/` | Customer purchasing and order analysis |
| `daily_orders/` | Daily order trends and sales activity |
| `delivery_performance/` | Order delivery and fulfillment analysis |
| `product_performance/` | Product-level sales and order analysis |

These tables are designed to support downstream SQL analysis and business intelligence reporting.

## AWS Infrastructure

Terraform provisions and manages the core AWS infrastructure used by the project, including:

- Amazon S3 data lake bucket.
- S3 versioning.
- Server-side encryption.
- S3 public access blocking.
- IAM role and permissions for AWS Glue.
- AWS Glue Data Catalog database.
- AWS Glue crawler.

**AWS Region:** `us-east-1`

**Glue database:** `cloudlake_catalog`

**S3 bucket:** `cloudlake-34081b81`

The bucket contains separate prefixes for the Bronze, Silver, and Gold layers, as well as Athena query results.

## Repository Structure

```text
cloudlake-terraform-aws/
├── data/                       # Local source datasets (not committed)
├── src/
│   ├── ingestion.py            # Bronze-layer ingestion
│   └── transform_to_silver.py  # Silver-layer transformation
├── terraform/
│   ├── provider.tf
│   ├── variables.tf
│   ├── s3.tf
│   ├── iam.tf
│   ├── glue.tf
│   └── outputs.tf
├── sql/
│   └── gold/                   # Gold-layer SQL scripts
├── requirements.txt
├── .gitignore
└── README.md
```

<img width="322" height="445" alt="Screenshot 2026-10-14 204244" src="https://github.com/user-attachments/assets/f53b4e5c-6b48-4dde-853e-54d788c0f56b" />

## Getting Started

### Prerequisites

- An AWS account with the required permissions.
- Terraform installed.
- Python installed.
- AWS CLI configured.
- Access to the Olist dataset on Kaggle.

### 1. Clone the repository

```bash
git clone https://github.com/okposomike/cloudlake-terraform-aws.git
cd cloudlake-terraform-aws
```

Confirm the repository URL matches your GitHub repository.

### 2. Configure AWS credentials

Configure credentials using an AWS CLI profile, environment variables, or another supported AWS credential method.

Verify your identity:

```bash
aws sts get-caller-identity
```

Never hardcode AWS credentials or commit secrets to GitHub.

### 3. Provision the infrastructure

```bash
cd terraform
terraform init
terraform fmt
terraform validate
terraform plan
terraform apply
```

Review the execution plan before applying changes. If the infrastructure already exists, use the correct Terraform state and configuration to avoid unintended changes.

### 4. Prepare the source data

Download the required Olist CSV files and place them in the project's local `data/` directory.

Keep raw datasets and sensitive files out of version control unless there is a specific reason to publish them.

### 5. Install Python dependencies

From the project root, run:

```bash
pip install -r requirements.txt
```

Ensure `requirements.txt` includes the actual libraries used by the scripts, such as `boto3`, `pandas`, and `pyarrow` if required.

### 6. Ingest the raw data

```bash
python src/ingestion.py
```

This uploads the source datasets into the Bronze layer in Amazon S3.

### 7. Transform the data

```bash
python src/transform_to_silver.py
```

This cleans the source datasets, converts them into Parquet files, and uploads the results to the Silver layer.

### 8. Update the Glue Catalog

Start the configured crawler:

```bash
aws glue start-crawler --name cloudlake-silver-crawler
```

Wait for the crawler to finish before querying updated tables in Athena.

### 9. Build and query the Gold layer

Open Amazon Athena, select the `cloudlake_catalog` database, and execute the Gold SQL scripts.

The CTAS (`CREATE TABLE AS SELECT`) statements create cataloged analytical tables and store their Parquet data in the specified Gold S3 locations.

Athena query-result storage is configured separately from the Gold table locations.

## Data Quality and Validation

Recommended validation checks include:

- Confirming that all nine datasets are present in Bronze.
- Comparing row counts before and after transformation.
- Checking for duplicate records and null business keys.
- Verifying date and timestamp conversions.
- Reconciling Gold aggregates against Silver data.
- Confirming that each Gold table returns expected records in Athena.
- Verifying that each Gold S3 folder contains the expected Parquet files.

## Project Status

- [x] AWS infrastructure provisioned using Terraform.
- [x] Raw data ingestion into Amazon S3.
- [x] Silver-layer transformation to Parquet.
- [x] AWS Glue database and crawler configured.
- [x] Silver datasets available for Athena queries.
- [x] Four Gold analytical tables modeled.
- [x] Gold data organized into separate S3 prefixes.
- [x] Project changes pushed to a GitHub feature branch.
- [ ] Data-quality validation and results documented.
- [ ] Setup instructions tested from a clean checkout.
- [ ] Automated testing and CI/CD improvements.

## Future Improvements

- Implement automated data-quality tests.
- Improve logging, retries, and error handling.
- Add GitHub Actions for code validation and testing.
- Introduce pipeline orchestration and scheduling.
- Connect the Gold tables to Power BI for interactive dashboards.
- Document data lineage and business metric definitions.

## Key Learning Outcomes

Through CloudLake, I have gained hands-on experience with:

- Infrastructure as Code using Terraform.
- Cloud object storage with Amazon S3.
- Python-based data ingestion and transformation.
- Parquet as a columnar storage format.
- AWS Glue data cataloging.
- SQL analytics and data modeling with Amazon Athena.
- Bronze, Silver, and Gold data lake architecture.
- Version control and collaborative development using Git and GitHub.

## Author

**Michael Okposo**

- LinkedIn: https://www.linkedin.com/in/okposo-michael-b0b99224a/

CloudLake is part of my ongoing journey in cloud data engineering, focused on building practical projects that solve real data problems.
