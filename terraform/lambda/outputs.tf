output "get_companies_lambda_invoke_arn" {
    value = aws_lambda_function.get_companies_lambda.invoke_arn
}

output "get_companies_lambda_arn" {
    value = aws_lambda_function.get_companies_lambda.arn
}

output "save_company_lambda_invoke_arn" {
    value = aws_lambda_function.save_company_lambda.invoke_arn
}

output "save_company_lambda_arn" {
    value = aws_lambda_function.save_company_lambda.arn
}

output "push_contact_message_lambda_invoke_arn" {
    value = aws_lambda_function.push_contact_message_lambda.invoke_arn
}

output "push_contact_message_lambda_arn" {
    value = aws_lambda_function.push_contact_message_lambda.arn
}

output "get_company_details_by_id_lambda_arn" {
  value = aws_lambda_function.get_comany_details_lambda.arn
}

output "get_company_details_by_id_lambda_invoke_arn" {
  value = aws_lambda_function.get_comany_details_lambda.invoke_arn
}