####S3####
#S3 bucket for put files as JSON
resource "aws_s3_bucket" "csv_bucket" {
  bucket = "csv-bucket"
  force_destroy = true
}

data "aws_s3_bucket" "athena_query_s3_bucket"{
  count = var.environment == "qa" ? 0 : 1
  bucket= "aws-athena-query-results-s3"
}



resource "aws_s3_bucket" "athena_query_s3" {
  bucket = data.aws_s3_bucket.athena_query_s3_bucket[0].bucket
}



resource "aws_s3_bucket_public_access_block" "athena_query_s3" {
  bucket                  = data.aws_s3_bucket.athena_query_s3_bucket[0].id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}