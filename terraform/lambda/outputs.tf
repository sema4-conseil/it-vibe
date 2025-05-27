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

output "patch_company_lambda_invoke_arn" {
    value = aws_lambda_function.patch_company_lambda.invoke_arn
}

output "patch_company_lambda_arn" {
    value = aws_lambda_function.patch_company_lambda.arn
}

output "get_contact_messages_lambda_invoke_arn" {
    value = aws_lambda_function.get_contact_messages_lambda.invoke_arn
}
output "get_contact_messages_lambda_arn" {
    value = aws_lambda_function.get_contact_messages_lambda.arn
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

output "delete_company_by_id_lambda_arn" {
  value = aws_lambda_function.delete_company_lambda.arn
}

output "delete_company_by_id_lambda_invoke_arn" {
  value = aws_lambda_function.delete_company_lambda.invoke_arn
}

output "get_reviews_by_company_id_lambda_arn" {
  value = aws_lambda_function.get_reviews_by_company_id_lambda.arn
}

output "get_reviews_by_company_id_lambda_invoke_arn" {
  value = aws_lambda_function.get_reviews_by_company_id_lambda.invoke_arn
}

output "add_review_lambda_arn" {
  value = aws_lambda_function.add_review_lambda.arn
}

output "add_review_lambda_invoke_arn" {
  value = aws_lambda_function.add_review_lambda.invoke_arn
}

output "get_company_metrics_lambda_arn" {
  value = aws_lambda_function.get_company_review_metrics_lambda.arn
}

output "get_company_metrics_lambda_invoke_arn" {
  value = aws_lambda_function.get_company_review_metrics_lambda.invoke_arn
}

output "patch_contact_messages_lambda_arn" {
  value = aws_lambda_function.patch_contact_messages_lambda.arn
}

output "patch_contact_messages_lambda_invoke_arn" {
  value = aws_lambda_function.patch_contact_messages_lambda.invoke_arn
}

output "import_companies_lambda_arn" {
  value = aws_lambda_function.import_companies_lambda.arn
}

output "import_companies_lambda_invoke_arn" {
  value = aws_lambda_function.import_companies_lambda.invoke_arn
}



output "health_check_lambda_arn" {
  value = aws_lambda_function.health_check_lambda.arn
}

output "health_check_lambda_invoke_arn" {
  value = aws_lambda_function.health_check_lambda.invoke_arn
}
