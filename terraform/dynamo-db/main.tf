resource "aws_dynamodb_table" "companies" {
  name           = "IT_VIBE_DEV_COMPANIES"
  billing_mode   = "PAY_PER_REQUEST" # On-demand capacity mode
  hash_key       = "id"
  attribute {
    name = "id" 
    type = "S" # String type
  }
}

  output "companies_table_arn" {
    value = aws_dynamodb_table.companies.arn
  }