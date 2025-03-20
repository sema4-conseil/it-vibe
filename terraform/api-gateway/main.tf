data "template_file" "itvibe_api_spec" {
  template = file(var.openapi_spec_location)

  vars = {
    get_companies_lambda_invoke_arn = var.get_companies_lambda_invoke_arn
    create_company_lambda_invoke_arn = var.save_company_lambda_invoke_arn
  }
}

resource "aws_api_gateway_rest_api" "itvibe_api" {
  name        = "ItVibeAPI"
  description = "API for IT-Vibe"
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

resource "aws_api_gateway_deployment" "deployment" {
  # depends_on = [aws_api_gateway_integration.get_companies_integration]
  rest_api_id = aws_api_gateway_rest_api.itvibe_api.id
}

resource "aws_api_gateway_stage" "stage" {
  stage_name = "dev"
  rest_api_id = aws_api_gateway_rest_api.itvibe_api.id
  deployment_id = aws_api_gateway_deployment.deployment.id
}
