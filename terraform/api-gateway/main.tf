data "template_file" "itvibe_api_spec" {
  template = file(var.openapi_spec_location)

  vars = {
    get_companies_lambda_invoke_arn = var.get_companies_lambda_invoke_arn
    create_company_lambda_invoke_arn = var.save_company_lambda_invoke_arn
    push_contact_message_lambda_invoke_arn = var.push_contact_message_lambda_invoke_arn
  }
}

variable "certeficate_arn" {
  default = "arn:aws:acm:eu-west-3:327441465709:certificate/47169326-35c6-49a7-9030-d361cff2184e"
}

variable "hosted_zone_id" {
  type = string
  description = "The zone id of the hosted zone"
}

resource "aws_api_gateway_rest_api" "itvibe_api" {
  name        = "api.it-vibe.sema4-conseil.com"
  description = "API for IT-Vibe backend"
  endpoint_configuration {
    types = ["REGIONAL"]
  }
  body = data.template_file.itvibe_api_spec.rendered
}

resource "aws_lambda_permission" "get_companies_lambda_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name =  var.get_companies_lambda_arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.itvibe_api.execution_arn}/*/*"
}

resource "aws_lambda_permission" "create_company_lambda_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name =  var.save_company_lambda_arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.itvibe_api.execution_arn}/*/*"
}

resource "aws_lambda_permission" "push_contact_message_lambda_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name =  var.push_contact_message_lambda_arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.itvibe_api.execution_arn}/*/*"
}

resource "aws_api_gateway_deployment" "deployment" {
  # depends_on = [aws_api_gateway_integration.get_companies_integration]
  rest_api_id = aws_api_gateway_rest_api.itvibe_api.id
}

resource "aws_api_gateway_stage" "dev_stage" {
  stage_name = "dev"
  rest_api_id = aws_api_gateway_rest_api.itvibe_api.id
  deployment_id = aws_api_gateway_deployment.deployment.id
}


resource "aws_api_gateway_domain_name" "dev_api_domain_name" {
  domain_name     = "dev.api.it-vibe.sema4-conseil.com"
   endpoint_configuration {
    types = ["REGIONAL"]
  }
  regional_certificate_arn = var.certeficate_arn
}

resource "aws_route53_record" "dev_api_route53_record" {
  zone_id = var.hosted_zone_id
  name    = aws_api_gateway_domain_name.dev_api_domain_name.domain_name
  type    = "A"
  alias {
    name = aws_api_gateway_domain_name.dev_api_domain_name.regional_domain_name
    zone_id = aws_api_gateway_domain_name.dev_api_domain_name.regional_zone_id
    evaluate_target_health = true
  }
}

resource "aws_api_gateway_base_path_mapping" "dev_api_domain_mapping" {
  api_id      = aws_api_gateway_rest_api.itvibe_api.id
  stage_name  = aws_api_gateway_stage.dev_stage.stage_name
  domain_name = aws_api_gateway_domain_name.dev_api_domain_name.domain_name
}