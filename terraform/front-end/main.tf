variable "hosted_zone_id" {}

resource "aws_s3_bucket" "it-vibe-static-site-s3" {
  bucket = "it-vibe.dev.sema4-conseil.com"
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
  source   = "../it-vibe-fe/dist/index.html"
  bucket = aws_s3_bucket.it-vibe-static-site-s3.id
  content_type = "text/html"
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_s3_object" "favicon" {
  key      = "favicon.ico"
  source   = "../it-vibe-fe/dist/favicon.ico"
  bucket = aws_s3_bucket.it-vibe-static-site-s3.id
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_s3_object" "js" {
  for_each = fileset("../it-vibe-fe/dist/js", "**/*.*")
  bucket      = aws_s3_bucket.it-vibe-static-site-s3.id
  key         = "js/${each.value}"
  source      = "../it-vibe-fe/dist/js/${each.value}"
  content_type = "application/javascript"
}

resource "aws_s3_object" "css" {
  for_each = fileset("../it-vibe-fe/dist/css", "**/*.*")
  bucket      = aws_s3_bucket.it-vibe-static-site-s3.id
  key         = "css/${each.value}"
  source      = "../it-vibe-fe/dist/css/${each.value}"
  content_type = "text/css"
  lifecycle {
    create_before_destroy = true
  }
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

// Create a route 53 for the static web-site
resource "aws_route53_record" "s3_static_site" {
  zone_id = var.hosted_zone_id
  name    = aws_s3_bucket_website_configuration.it-vibe-static-site-s3-configuration.bucket
  type    = "A"
  alias {
    name = aws_s3_bucket_website_configuration.it-vibe-static-site-s3-configuration.website_domain
    zone_id = aws_s3_bucket.it-vibe-static-site-s3.hosted_zone_id 
    evaluate_target_health = "true"
  }
}