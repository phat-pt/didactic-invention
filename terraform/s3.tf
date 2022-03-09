####S3####
#S3 bucket for put files as JSON
resource "aws_s3_bucket" "csv_bucket" {
  bucket = "csv-bucket"
  force_destroy = true
}
