provider "aws" {
  region = "eu-west-3"
}

resource "aws_s3_bucket" "it-vibe-static-site-s3" {
  bucket = "it-vibe-static-site-s3"
  tags = {
    Name = "IT-Vibe-s3-bucket-static-web-site"
    Env = "dev"
  }
}

resource "aws_s3_bucket_public_access_block" "public-access" {
  bucket = aws_s3_bucket.it-vibe-static-site-s3.id
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "allow-public-access-bucket-policy" {
  bucket = aws_s3_bucket.it-vibe-static-site-s3.id
  policy = data.aws_iam_policy_document.public-policy-json.json
}

data "aws_iam_policy_document" "public-policy-json" {
  statement {
    principals {
      identifiers = [ "*" ]
      type = "*"
    }
    actions = [
      "s3:GetObject",
      "s3:ListBucket",
    ]

    resources = [
      aws_s3_bucket.it-vibe-static-site-s3.arn,
      "${aws_s3_bucket.it-vibe-static-site-s3.arn}/*",
    ]
  }
}


resource "aws_s3_object" "index-html" {
  key      = "index.html"
  source   = "../dist/index_2.html"
  bucket = aws_s3_bucket.it-vibe-static-site-s3.id
  content_type = "text/html"
}



resource "aws_s3_bucket_website_configuration" "it-vibe-static-site-s3-configuration" {
  bucket = aws_s3_bucket.it-vibe-static-site-s3.id
  index_document {
    suffix = "index.html"
  }
  error_document {
    key = "error.html"
  }

}

output "bucket_arn" { 
  value = aws_s3_bucket.it-vibe-static-site-s3.arn
}

output "site-endpoint" {
  value = aws_s3_bucket_website_configuration.it-vibe-static-site-s3-configuration.website_endpoint
}