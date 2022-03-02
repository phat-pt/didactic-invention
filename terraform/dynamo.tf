#DynamoDB
resource "aws_dynamodb_table" "dynamob_counting_table" {
  name           = "csv_count_table"
  billing_mode = "PAY_PER_REQUEST"
  hash_key       = "row"
  attribute {
    name = "row"
    type = "N"
  }
}