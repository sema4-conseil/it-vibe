variable "hosted_zone_id" {}
variable "env" {}
variable "region" {}
variable "certeficate_arn" {}

locals {
  # bucket name is "it-vibe.${var.env}.sema4-conseil.com" if env is not prod  else it-vibe.sema4-conseil.com
  s3_name        = var.env == "prod" ? "it-vibe.sema4-conseil.com" : "it-vibe.${var.env}.sema4-conseil.com"
  s3_origin_id   = var.env == "prod" ? "it-vibe.sema4-conseil.com-origin" : "it-vibe.${var.env}.sema4-conseil.com-origin"
  s3_domain_name = var.env == "prod" ? "it-vibe.sema4-conseil.com.s3-website.${var.region}.amazonaws.com" : "it-vibe.${var.env}.sema4-conseil.com.s3-website.${var.region}.amazonaws.com"
}


resource "aws_s3_bucket" "it-vibe-static-site-s3" {
  bucket = local.s3_name
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
  # Try to get the filemd5, fall back to empty string if file doesn't exist
  etag = try(filemd5("../it-vibe-fe/dist/index.html"),"")
}

resource "aws_s3_object" "favicon" {
  key      = "favicon.ico"
  source   = "../it-vibe-fe/dist/favicon.ico"
  bucket = aws_s3_bucket.it-vibe-static-site-s3.id
  lifecycle {
    create_before_destroy = true
  }
  # Try to get the filemd5, fall back to empty string if file doesn't exist
  etag = try(filemd5("../it-vibe-fe/dist/favicon.ico"),"")
}

resource "aws_s3_object" "js" {
  for_each = fileset("../it-vibe-fe/dist/js", "**/*.*")
  bucket      = aws_s3_bucket.it-vibe-static-site-s3.id
  key         = "js/${each.value}"
  source      = "../it-vibe-fe/dist/js/${each.value}"
  content_type = "application/javascript"
  # Try to get the filemd5, fall back to empty string if file doesn't exist
  etag = try(filemd5("../it-vibe-fe/dist/js/${each.value}"),"")
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
  # Try to get the filemd5, fall back to empty string if file doesn't exist
  etag = try(filemd5("../it-vibe-fe/dist/css/${each.value}"),"")
}



resource "aws_s3_bucket_website_configuration" "it-vibe-static-site-s3-configuration" {
  bucket = aws_s3_bucket.it-vibe-static-site-s3.id
  index_document {
    suffix = "index.html"
  }
  error_document {
    key = "index.html"
  }

}

// CloudFront
// Create a CloudFront distribution for the static website
// The distribution will use the S3 bucket as the origin
// The distribution will be configured to use HTTPS and redirect HTTP requests to HTTPS
// The distribution will also be configured to use a custom domain name

resource "aws_cloudfront_distribution" "cloudfront_distribution" {
  count = var.env == "prod" ? 1 : 0
  aliases = ["it-vibe.sema4-conseil.com"]
  origin {
    origin_id                = local.s3_origin_id
    domain_name              = local.s3_domain_name

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols   = ["TLSv1.2", "TLSv1.1"]
    }
  }
  enabled             = true
  is_ipv6_enabled      = true
  comment              = "[${var.env}] it-vibe static web-site"
  default_root_object  = "index.html"

  default_cache_behavior {
    compress = true  # Enable gzip/brotli compression
    target_origin_id       = local.s3_origin_id
    viewer_protocol_policy = "redirect-to-https"

    allowed_methods = ["GET", "HEAD"]
    cached_methods  = ["GET", "HEAD"]

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    min_ttl     = 3600      # 1 hour (minimum cache time)
    default_ttl = 86400     # 1 day (default cache time)
    max_ttl     = 604800    # 7 days (maximum cache time)
    

  }

  # Since most traffic is from France, downgrade to PriceClass_200 (Europe, North America, and parts of Asia) instead of PriceClass_100 (global).
  price_class = "PriceClass_200"

  # Since your audience is primarily in France
  restrictions {
    geo_restriction {
      restriction_type = "whitelist"
      locations        = ["FR"]
    }
  }

  viewer_certificate {
    acm_certificate_arn      = "arn:aws:acm:us-east-1:327441465709:certificate/c5f040cf-ff62-4309-b1d3-f85a4631a8df"
    ssl_support_method        = "sni-only"
    minimum_protocol_version  = "TLSv1.2_2021" # Use the latest protocol version
  }
}

resource "null_resource" "invalidate_cloudfront" {
  # This resource is used to invalidate the CloudFront cache when the S3 bucket content changes
  count = var.env == "prod" ? 1 : 0
  triggers = {
    # Trigger invalidation when files change
    run_id = timestamp()
  }

  provisioner "local-exec" {
    command = <<EOT
      aws cloudfront create-invalidation --distribution-id ${aws_cloudfront_distribution.cloudfront_distribution[0].id} --paths /* /.
    EOT
  }
}

// Create a route 53 for the static web-site
resource "aws_route53_record" "s3_static_site" {
  count = var.env == "prod" ? 1 : 0
  zone_id = var.hosted_zone_id
  name    = "it-vibe.sema4-conseil.com"
  type    = "A"
   alias {
    name                   = aws_cloudfront_distribution.cloudfront_distribution[0].domain_name
    zone_id                = aws_cloudfront_distribution.cloudfront_distribution[0].hosted_zone_id
    evaluate_target_health = false
  }
}