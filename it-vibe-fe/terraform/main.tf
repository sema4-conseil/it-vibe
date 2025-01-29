provider "aws" {
  region = "eu-west-3"
}

terraform {
  backend "s3" {
    bucket         = "it-vibe-terraform-backend-state"
    key            = "it-vibe/terraform.tfstate"
    region         = "eu-west-3" 
    encrypt        = true
  }
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
  depends_on = [ aws_s3_bucket_public_access_block.public-access ]
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
  source   = "../dist/index.html"
  bucket = aws_s3_bucket.it-vibe-static-site-s3.id
  content_type = "text/html"
}

resource "aws_s3_object" "favicon" {
  key      = "favicon.ico"
  source   = "../dist/favicon.ico"
  bucket = aws_s3_bucket.it-vibe-static-site-s3.id
}

resource "aws_s3_object" "js" {
  for_each = fileset("../dist/js", "**/*.*")
  bucket      = aws_s3_bucket.it-vibe-static-site-s3.id
  key         = "js/${each.value}"
  source      = "../dist/js/${each.value}"
  content_type = "application/javascript"
}

resource "aws_s3_object" "css" {
  for_each = fileset("../dist/css", "**/*.*")
  bucket      = aws_s3_bucket.it-vibe-static-site-s3.id
  key         = "css/${each.value}"
  source      = "../dist/css/${each.value}"
  content_type = "text/css"
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