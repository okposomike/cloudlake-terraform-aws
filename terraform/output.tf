output "data_lake_bucket_name" {
  description = "Name of the CloudLake S3 bucket"
  value       = aws_s3_bucket.data_lake.bucket
}

output "data_lake_bucket_arn" {
  description = "ARN of the CloudLake S3 bucket"
  value       = aws_s3_bucket.data_lake.arn
}

output "data_lake_bucket_region" {
  description = "AWS region of the data lake"
  value       = var.aws_region
}