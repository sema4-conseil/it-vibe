provider "aws" {
  region = "eu-west-3"
  default_tags {
    tags = {
      Env =  var.env
      ManagedBy   = "Terraform"
      Version = var.be_version
      DeployedBy = var.deployed_by
    }
  }
}

terraform {
  backend "s3" {
    bucket         = "it-vibe-terraform-backend-state"
    key            = "it-vibe/terraform.tfstate"
    region         = "eu-west-3" 
    encrypt        = true
  }
}

variable "deployed_by" {
  type = string
  default = "manual"
}

variable "hosted_zone_id" {
  default = "Z09606333IIM9GKOYXW0S"
}

variable "account_id" {
  type = string
  default = "327441465709"
}

variable "region" {
  type = string
  default = "eu-west-3"
}

variable "env" {
  type = string
  description = "The environment name"
}

variable "log_level" {
  type = string
  default = "INFO"
  description = "The log level for the application"
}

variable "be_version" {
  type = string
  description = "The backend version"
}

variable "certeficate_arn" {
  default = "arn:aws:acm:eu-west-3:327441465709:certificate/a84734ce-fc81-4ec5-b0a9-9ff30111831c"
}


module "front-end" {
  source = "./front-end"
  hosted_zone_id = var.hosted_zone_id
  env = var.env
  region = var.region
  certeficate_arn = var.certeficate_arn
}

module "lambda" {
  source = "./lambda"
  env = var.env
  be_version = var.be_version
  log_level = var.log_level

  contact_message_stream_arn = module.dynamo-db.contact_message_stream_arn
}

module "dynamo-db" {
  source = "./dynamo-db"
  env = var.env
}

module "api-gateway" {
  depends_on = [ module.lambda ]
  account_id = var.account_id
  region = var.region
  env = var.env
  source = "./api-gateway"
  openapi_spec_location = "../it-vibe-be/open-api/itvibe-api.yaml"
  hosted_zone_id = var.hosted_zone_id
  certeficate_arn = var.certeficate_arn
  health_check_lambda_arn = module.lambda.health_check_lambda_arn
  health_check_lambda_invoke_arn = module.lambda.health_check_lambda_invoke_arn
  get_companies_lambda_invoke_arn = module.lambda.get_companies_lambda_invoke_arn
  get_companies_lambda_arn = module.lambda.get_companies_lambda_arn
  save_company_lambda_invoke_arn = module.lambda.save_company_lambda_invoke_arn
  save_company_lambda_arn = module.lambda.save_company_lambda_arn
  patch_company_lambda_invoke_arn = module.lambda.patch_company_lambda_invoke_arn
  patch_company_lambda_arn = module.lambda.patch_company_lambda_arn
  get_company_details_by_id_lambda_arn = module.lambda.get_company_details_by_id_lambda_arn
  get_company_details_by_id_lambda_invoke_arn = module.lambda.get_company_details_by_id_lambda_invoke_arn
  get_company_metrics_lambda_arn = module.lambda.get_company_metrics_lambda_arn
  get_company_metrics_lambda_invoke_arn = module.lambda.get_company_metrics_lambda_invoke_arn
  delete_company_by_id_lambda_arn = module.lambda.delete_company_by_id_lambda_arn
  delete_company_by_id_lambda_invoke_arn = module.lambda.delete_company_by_id_lambda_invoke_arn
  push_contact_message_lambda_arn = module.lambda.push_contact_message_lambda_arn
  push_contact_message_lambda_invoke_arn = module.lambda.push_contact_message_lambda_invoke_arn
  get_contact_messages_lambda_invoke_arn = module.lambda.get_contact_messages_lambda_invoke_arn
  get_contact_messages_lambda_arn = module.lambda.get_contact_messages_lambda_arn
  patch_contact_messages_lambda_arn = module.lambda.patch_contact_messages_lambda_arn
  patch_contact_messages_lambda_invoke_arn = module.lambda.patch_contact_messages_lambda_invoke_arn
  get_reviews_by_company_id_lambda_arn = module.lambda.get_reviews_by_company_id_lambda_arn
  get_reviews_by_company_id_lambda_invoke_arn = module.lambda.get_reviews_by_company_id_lambda_invoke_arn
  add_review_lambda_invoke_arn = module.lambda.add_review_lambda_invoke_arn
  add_review_lambda_arn = module.lambda.add_review_lambda_arn
  import_companies_lambda_invoke_arn = module.lambda.import_companies_lambda_invoke_arn
  import_companies_lambda_arn = module.lambda.import_companies_lambda_arn
  delete_review_lambda_arn = module.lambda.delete_review_lambda_arn
  delete_review_lambda_invoke_arn = module.lambda.delete_review_lambda_invoke_arn
  transform_review_lambda_arn = module.lambda.transform_review_lambda_arn
  transform_review_lambda_invoke_arn = module.lambda.transform_review_lambda_invoke_arn
}
