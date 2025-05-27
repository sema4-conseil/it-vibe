resource "aws_lambda_permission" "lambda_permission" {
  for_each = {
    "get_companies"               = var.get_companies_lambda_arn
    "save_company"                = var.save_company_lambda_arn
    "patch_company"                = var.patch_company_lambda_arn
    "get_company_details_by_id"   = var.get_company_details_by_id_lambda_arn
    "delete_company_by_id"        = var.delete_company_by_id_lambda_arn
    "push_contact_message"        = var.push_contact_message_lambda_arn
    "get_contact_messages"        = var.get_contact_messages_lambda_arn
    "patch_contact_message"       = var.patch_contact_messages_lambda_arn
    "get_reviews_by_company_id"   = var.get_reviews_by_company_id_lambda_arn
    "add_review"                  = var.add_review_lambda_arn
    "get_company_metrics"         = var.get_company_metrics_lambda_arn
    "health_check"                = var.health_check_lambda_arn
    "import_companies"            = var.import_companies_lambda_arn
  }

  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name =  each.value
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.itvibe_api.execution_arn}/*/*"
}

data "template_file" "itvibe_api_spec" {
  template = file(var.openapi_spec_location)

  vars = {
    health_check_lambda_invoke_arn                = var.health_check_lambda_invoke_arn
    get_companies_lambda_invoke_arn               = var.get_companies_lambda_invoke_arn
    create_company_lambda_invoke_arn              = var.save_company_lambda_invoke_arn
    import_companies_lambda_invoke_arn            = var.import_companies_lambda_invoke_arn
    patch_company_lambda_invoke_arn               = var.patch_company_lambda_invoke_arn
    push_contact_message_lambda_invoke_arn        = var.push_contact_message_lambda_invoke_arn
    get_contact_messages_lambda_invoke_arn        = var.get_contact_messages_lambda_invoke_arn
    patch_contact_message_lambda_invoke_arn       = var.patch_contact_messages_lambda_invoke_arn
    get_company_details_by_id_lambda_invoke_arn   = var.get_company_details_by_id_lambda_invoke_arn
    delete_company_by_id_lambda_invoke_arn        = var.delete_company_by_id_lambda_invoke_arn
    get_company_metrics_lambda_invoke_arn         = var.get_company_metrics_lambda_invoke_arn
    get_reviews_by_company_id_lambda_invoke_arn   = var.get_reviews_by_company_id_lambda_invoke_arn
    add_review_lambda_invoke_arn                  = var.add_review_lambda_invoke_arn
  }
}


resource "aws_api_gateway_rest_api" "itvibe_api" {
  name        = "api.it-vibe.sema4-conseil.com"
  description = "it-vibe api for ${var.env} environment"
  endpoint_configuration {
    types = ["REGIONAL"]
  }
  body = data.template_file.itvibe_api_spec.rendered
}


resource "aws_api_gateway_deployment" "deployment" {
  rest_api_id = aws_api_gateway_rest_api.itvibe_api.id
}

resource "aws_api_gateway_account" "api_gateway_account" {
  cloudwatch_role_arn = "arn:aws:iam::327441465709:role/ApiGatewayCloudwatch"
}

resource "aws_api_gateway_stage" "api_gateway_stage" {
  stage_name = "${var.env}"
  rest_api_id = aws_api_gateway_rest_api.itvibe_api.id
  deployment_id = aws_api_gateway_deployment.deployment.id

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gateway_logs.arn
    format = jsonencode({
		# Existing fields
		requestId         = "$context.requestId"
		ip                = "$context.identity.sourceIp"
		caller            = "$context.identity.caller"
		user              = "$context.identity.user"
		requestTime       = "$context.requestTime"
		httpMethod        = "$context.httpMethod"
		resourcePath      = "$context.resourcePath"
		status            = "$context.status"
		protocol          = "$context.protocol"
		responseLength    = "$context.responseLength"
		integrationError  = "$context.integration.error"
		
		# New fields
		userAgent         = "$context.identity.userAgent"
		responseLatency   = "$context.responseLatency"
		integrationLatency= "$context.integration.latency"
		domainName        = "$context.domainName"
		errorMessage      = "$context.error.message"
		apiKeyId          = "$context.identity.apiKeyId"
		requestTimeEpoch  = "$context.requestTimeEpoch"
    })
  }

  # Enable detailed CloudWatch metrics and logging
  xray_tracing_enabled = true  # Optional: Enable X-Ray tracing
}

resource "aws_cloudwatch_log_group" "api_gateway_logs" {
  name              = "itvibe_api_gateway_${aws_api_gateway_rest_api.itvibe_api.id}/${var.env}"
  retention_in_days = 1 
}


resource "aws_api_gateway_domain_name" "api_domain_name" {
  domain_name     = var.env == "prod" ? "api.it-vibe.sema4-conseil.com" : "${var.env}.api.it-vibe.sema4-conseil.com"
   endpoint_configuration {
    types = ["REGIONAL"]
  }
  regional_certificate_arn = var.certeficate_arn
}

resource "aws_route53_record" "api_route53_record" {
  zone_id = var.hosted_zone_id
  name    = aws_api_gateway_domain_name.api_domain_name.domain_name
  type    = "A"
  alias {
    name = aws_api_gateway_domain_name.api_domain_name.regional_domain_name
    zone_id = aws_api_gateway_domain_name.api_domain_name.regional_zone_id
    evaluate_target_health = true
  }
}

resource "aws_api_gateway_base_path_mapping" "api_domain_mapping" {
  api_id      = aws_api_gateway_rest_api.itvibe_api.id
  stage_name  = aws_api_gateway_stage.api_gateway_stage.stage_name
  domain_name = aws_api_gateway_domain_name.api_domain_name.domain_name
}