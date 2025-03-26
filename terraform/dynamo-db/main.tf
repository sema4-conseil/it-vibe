resource "aws_dynamodb_table" "companies" {
  name           = "IT_VIBE_DEV_COMPANIES"
  billing_mode   = "PAY_PER_REQUEST" # On-demand capacity mode

  hash_key       = "id"
  range_key      = "name"

  attribute {
    name = "id" 
    type = "S" # String type
  }

  attribute {
    name = "name"
    type = "S" # String type
  }
  # No Global Secondary Indexes (GSI) or Local Secondary Indexes (LSI) specified.
}

  output "companies_table_arn" {
    value = aws_dynamodb_table.companies.arn
  }