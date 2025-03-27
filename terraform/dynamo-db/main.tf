resource "aws_dynamodb_table" "companies" {
  name           = "IT_VIBE_DEV_COMPANIES"
  billing_mode   = "PAY_PER_REQUEST" # On-demand capacity mode
  hash_key       = "id"
  attribute {
    name = "id" 
    type = "S" # String type
  }
}

resource "aws_dynamodb_table" "company_reviews" {
  name           = "IT_VIBE_DEV_COMPANY_REVIEWS"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "company_id"
  range_key      = "review_id" # To ensure uniqueness of reviews per company

  attribute {
    name = "company_id"
    type = "S"
  }

  attribute {
    name = "review_id"
    type = "S"
  }

  attribute {
    name = "rating"
    type = "N" 
  }

  /**
    * Global Secondary Index (GSI) to query reviews by rating
    * it could be very useful if you wanted to get the reviews sorted by rating for a specific company, 
    * or if you wanted to query for companies with a specific rating.
    */
  global_secondary_index {
    name            = "RatingIndex"
    hash_key        = "company_id"
    range_key       = "rating"
    projection_type = "ALL"
  }

  tags = {
    Name        = "IT_VIBE_DEV_COMPANY_REVIEWS"
    Environment = "dev"
    ManagedBy   = "Terraform"
  }
}

  output "companies_table_arn" {
    value = aws_dynamodb_table.companies.arn
  }

  output "company_reviews_table_arn" {
    value = aws_dynamodb_table.company_reviews.arn
  }