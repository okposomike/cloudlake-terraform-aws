resource "random_id" "bucket_suffix" {
  byte_length = 4
}

resource "aws_s3_bucket" "data_lake" {
  bucket = "${var.project_name}-${random_id.bucket_suffix.hex}"

  tags = {
    Project     = "CloudLake"
    Environment = "dev"
    ManagedBy   = "Terraform"
  }
}

resource "aws_s3_bucket_versioning" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_object" "bronze" {
  bucket  = aws_s3_bucket.data_lake.id
  key     = "bronze/"
  content = ""
}

resource "aws_s3_object" "silver" {
  bucket  = aws_s3_bucket.data_lake.id
  key     = "silver/"
  content = ""
}

resource "aws_s3_object" "gold" {
  bucket  = aws_s3_bucket.data_lake.id
  key     = "gold/"
  content = ""
}