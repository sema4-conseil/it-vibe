resource "aws_api_gateway_rest_api" "itvibe_api" {
  name        = "ItVibeAPI"
  description = "API for IT-Vibe"
  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

resource "aws_api_gateway_resource" "companies" {
  rest_api_id = aws_api_gateway_rest_api.itvibe_api.id
  parent_id   = aws_api_gateway_rest_api.itvibe_api.root_resource_id
  path_part   = "companies"
}

resource "aws_api_gateway_method" "get_companies" {
  rest_api_id   = aws_api_gateway_rest_api.itvibe_api.id
  resource_id   = aws_api_gateway_resource.companies.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "get_companies_integration" {
  rest_api_id             = aws_api_gateway_rest_api.itvibe_api.id
  resource_id             = aws_api_gateway_resource.companies.id
  http_method             = aws_api_gateway_method.get_companies.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = var.get_compagnies_lambda_invoke_arn
}

resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name =  var.get_compagnies_lambda_arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.itvibe_api.execution_arn}/*/*"
}


resource "aws_api_gateway_method_response" "get_companies_method_response" {
  rest_api_id = aws_api_gateway_rest_api.itvibe_api.id
  resource_id = aws_api_gateway_resource.companies.id
  http_method = aws_api_gateway_method.get_companies.http_method
  response_models = {
    "application/json" = "Empty"
  }
  status_code = 200
}

resource "aws_api_gateway_integration_response" "integration_response" {
    rest_api_id = aws_api_gateway_rest_api.itvibe_api.id
    resource_id = aws_api_gateway_resource.companies.id
    http_method = aws_api_gateway_method.get_companies.http_method
    status_code = aws_api_gateway_method_response.get_companies_method_response.status_code
    response_templates = {
        "application/json" = <<EOF
        {
            [
  {
    "name": "Capgemeni",
    "location": "Pune",
    "code": "C1",
    "size": "1000"
  },
  {
    "name": "TCS",
    "location": "Mumbai",
    "code": "T1",
    "size": "2000"
  },
  {
    "name": "Infosys",
    "location": "Bangalore",
    "code": "I1",
    "size": "3000"
  },
  {
    "name": "Wipro",
    "location": "Chennai",
    "code": "W1",
    "size": "4000"
  }
]

        }
        EOF
    }
}

resource "aws_api_gateway_deployment" "deployment" {
  depends_on = [aws_api_gateway_integration.get_companies_integration]
  rest_api_id = aws_api_gateway_rest_api.itvibe_api.id
}

resource "aws_api_gateway_stage" "stage" {
  stage_name = "dev"
  rest_api_id = aws_api_gateway_rest_api.itvibe_api.id
  deployment_id = aws_api_gateway_deployment.deployment.id
}
