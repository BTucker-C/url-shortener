provider "aws" {
  region = var.aws_region
}

resource "aws_dynamodb_table" "url_links" {
  name         = "url-shortener-links"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "short_id"

  attribute {
    name = "short_id"
    type = "S"
  }

  tags = {
    Project = "URLShortener"
  }
}

resource "aws_iam_role" "lambda_role" {
  name = "url-shortener-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy" "lambda_dynamodb_policy" {
  name = "url-shortener-dynamodb-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:PutItem"
        ]
        Resource = aws_dynamodb_table.url_links.arn
      }
    ]
  })
}

resource "aws_lambda_function" "shorten_url" {
  function_name = "url-shortener-create-link"
  role          = aws_iam_role.lambda_role.arn
  handler       = "shorten_url.lambda_handler"
  runtime       = "python3.12"

  filename         = "../lambda/lambda.zip"
  source_code_hash = filebase64sha256("../lambda/lambda.zip")

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.url_links.name
      BASE_URL   = ""
    }
  }

  depends_on = [
    aws_iam_role_policy_attachment.lambda_basic_execution,
    aws_iam_role_policy.lambda_dynamodb_policy
  ]
}