####S3####
#S3 bucket for put files as JSON
resource "aws_s3_bucket" "csv_bucket" {
  bucket = "csv-bucket"
  force_destroy = true
}


resource "aws_s3_bucket" "query_s3" {
  count  = var.environment == "qa" ? 0 : 1
  bucket = "abc-s3"
}

resource "aws_s3_bucket_public_access_block" "query_s3_policy" {
  bucket = aws_s3_bucket.query_s3[0].id
  block_public_acls = true
  block_public_policy = true
  ignore_public_acls = true
  restrict_public_buckets = true
}
