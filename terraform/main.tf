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

module "front-end" {
  source = "./front-end"
}

module "lambda" {
  source = "./lambda"
}


module "api-gateway" {
  source = "./api-gateway"
  get_compagnies_lambda_invoke_arn = module.lambda.get_compagnies_lambda_invoke_arn
  get_compagnies_lambda_arn = module.lambda.get_compagnies_lambda_arn
  depends_on = [ module.lambda ]
}
