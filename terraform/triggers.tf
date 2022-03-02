#Add s3 resource for invoking to lambda function
resource "aws_s3_bucket_notification" "lambda_csv_count_trigger" {
   bucket = "${aws_s3_bucket.csv_bucket.id}"
   lambda_function {
       lambda_function_arn = "${aws_lambda_function.lambda_csv_count.arn}"
       events = ["s3:ObjectCreated:*"]
   }
   depends_on = [ aws_lambda_permission.lambda_csv_count_trigger_permission ]
}