resource "aws_glue_catalog_database" "cloudlake" {
  name        = "${var.project_name}_catalog"
  description = "Data catalog for the CloudLake data lake"

  tags = {
    Project   = "CloudLake"
    ManagedBy = "Terraform"
  }
}

resource "aws_glue_crawler" "silver" {
  name          = "${var.project_name}-silver-crawler"
  database_name = aws_glue_catalog_database.cloudlake.name
  role          = aws_iam_role.glue_role.arn

  s3_target {
    path = "s3://${aws_s3_bucket.data_lake.bucket}/silver/"
  }

  schema_change_policy {
    update_behavior = "UPDATE_IN_DATABASE"
    delete_behavior = "DEPRECATE_IN_DATABASE"
  }

  tags = {
    Project   = "CloudLake"
    ManagedBy = "Terraform"
  }
}