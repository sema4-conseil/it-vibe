variable "env" {}
resource "aws_dynamodb_table" "companies" {
  name           = "IT_VIBE_COMPANIES_${upper(var.env)}"
  billing_mode   = "PAY_PER_REQUEST" # On-demand capacity mode
  hash_key       = "id"
  attribute {
    name = "id" 
    type = "S"
  }

  attribute {
    name = "name_lowercase"
    type = "S" # String type (for case-insensitive search)
  }

  attribute {
    name = "country"
    type = "S"
  }

  attribute {
    name = "siren"
    type = "S"
  }

  attribute {
    name = "siret"
    type = "S"
  }

  global_secondary_index {
    name            = "siren-index"
    hash_key        = "siren"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "siret-index"
    hash_key        = "siret"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "country-index"
    hash_key        = "country"
    range_key       = "name_lowercase"
    projection_type = "ALL"
  }

  tags = {
    Entity      = "Company"
  }

}

resource "aws_dynamodb_table" "company_reviews" {
  name           = "IT_VIBE_COMPANY_REVIEWS_${upper(var.env)}"
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
      Entity      = "CompanyReview"
  }
}

resource "aws_dynamodb_table" "contact_messages" {
  name           = "IT_VIBE_CONTACT_MESSAGES_${upper(var.env)}"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "id"
  range_key      = "timestamp"
  stream_enabled = true
  stream_view_type = "NEW_IMAGE"
	attribute {
		name = "id"
		type = "S"
	}
	attribute {
		name = "timestamp"
		type = "N"
	}
  attribute {
    name = "status"
    type = "N" 
  }
  global_secondary_index {
    name            = "StatusTimestampIndex"
    hash_key        = "status"
    range_key       = "timestamp"
    projection_type = "ALL"
  }
  tags = {
      Entity      = "ContactMessage"
  }
}

output "contact_message_stream_arn" {
  value       = aws_dynamodb_table.contact_messages.stream_arn
  description = "The ARN of the DynamoDB stream for contact messages"
}