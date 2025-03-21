variable "zone_id" {
  description = "The zone id of the hosted zone"
  default = "Z09606333IIM9GKOYXW0S"
}


variable "s3_hosted_zone_id" {
  description = "value of the hosted zone id of static s3 site"
}

variable "s3_domain_name" {
  description = "value of the hosted zone id of static s3 site"
}

variable "bucket_name" {
 description = "value of the hosted zone id of static s3 site" 
}

resource "aws_route53_record" "s3_static_site" {
  zone_id = var.zone_id
  name    = var.bucket_name
  type    = "A"
  alias {
    name = var.s3_domain_name
    zone_id = var.s3_hosted_zone_id 
    evaluate_target_health = "true"
  }
}