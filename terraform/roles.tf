####IAM###
#LambdaExcecution IAM Policies

#LambdaExecution IAM Resources
resource "aws_iam_role" "lambda_csv_count_role" {
  name = "lambda_csv_count_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution_policy" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.lambda_csv_count_role.name
}

resource "aws_iam_role_policy" "lambda_csv_count_role_policy" {
  name = "lambda_csv_count_role_policy"
  role       = aws_iam_role.lambda_csv_count_role.name

policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "s3:ListBucket",
        "s3:GetObject",
        "s3:CopyObject",
        "s3:HeadObject"
      ],
      "Effect": "Allow",
      "Resource": [
        "arn:aws:s3:::${aws_s3_bucket.csv_bucket.id}",
        "arn:aws:s3:::${aws_s3_bucket.csv_bucket.id}/*"
      ]
    },
    {
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:GetRecords",
        "dynamodb:PutItem",
        "dynamodb:UpdateItem",
        "dynamodb:Query"
      ],
      "Effect": "Allow",
      "Resource": "${aws_dynamodb_table.dynamob_counting_table.arn}"
    }
  ]
}
EOF

}



#Grant bucket-1 permission to trigger Lambda Function
resource "aws_lambda_permission" "lambda_csv_count_trigger_permission" {
  statement_id = "AllowExecutionFromS3Bucket"
  action = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.lambda_csv_count.arn}"
  principal = "s3.amazonaws.com"
  source_arn = "${aws_s3_bucket.csv_bucket.arn}"
}
