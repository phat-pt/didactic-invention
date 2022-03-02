####Lambda Function###
#Lambda package data
data "archive_file" "lambda_csv_count" {
    type = "zip"
    source {
      content  = file("../src/lambda_csv_count.py")
      filename = "src/lambda_csv_count.py"
    }
    output_path = "./lambda_csv_count.zip"
    
}

#Lambda resource
resource "aws_lambda_function" "lambda_csv_count" {
  function_name = "lambda_csv_count"
  filename = "lambda_csv_count.zip"
  runtime = "python3.8"
  handler = "src/lambda_csv_count.lambda_handler"
  timeout = "900"
  memory_size = "128"
  source_code_hash = data.archive_file.lambda_csv_count.output_base64sha256
  role = aws_iam_role.lambda_csv_count_role.arn
}


