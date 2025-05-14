variable "certeficate_arn" {
  default = "arn:aws:acm:eu-west-3:327441465709:certificate/47169326-35c6-49a7-9030-d361cff2184e"
}

variable "hosted_zone_id" {
  type = string
  description = "The zone id of the hosted zone"
}

variable "account_id" {}
variable "region" {}
variable "env" {}

variable "get_companies_lambda_invoke_arn" {}
variable "get_companies_lambda_arn" {}
variable "save_company_lambda_invoke_arn" {}
variable "save_company_lambda_arn" {}
variable "get_company_details_by_id_lambda_invoke_arn" {}
variable "delete_company_by_id_lambda_arn" {}
variable "delete_company_by_id_lambda_invoke_arn" {}
variable "get_company_details_by_id_lambda_arn" {}
variable "get_company_metrics_lambda_arn" {}
variable "push_contact_message_lambda_arn" {}
variable "push_contact_message_lambda_invoke_arn" {}
variable "get_contact_messages_lambda_arn" {}
variable "get_contact_messages_lambda_invoke_arn" {}
variable "patch_contact_messages_lambda_arn" {}
variable "get_reviews_by_company_id_lambda_arn" {}
variable "get_reviews_by_company_id_lambda_invoke_arn" {} 
variable "add_review_lambda_arn" {}
variable "add_review_lambda_invoke_arn" {}

variable "openapi_spec_location"  {}
