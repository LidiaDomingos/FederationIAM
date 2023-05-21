terraform {

required_providers {

    aws = {

    source  = "hashicorp/aws"

    version = "~> 4.67.0"

    }

  }

}

provider "aws" {
    region     = "us-east-1"
    access_key = "${var.access_key}"
    secret_key = "${var.secret_key}"
}

resource "aws_iam_user" "users" {
  for_each = var.users

  name = each.value.name
  path = each.value.path
  tags = each.value.tags
}

resource "aws_iam_user_policy_attachment" "user_policies" {
  for_each = var.users

  user       = aws_iam_user.users[each.key].name
  policy_arn = each.value.policy_arns[0]
}

resource "aws_iam_access_key" "user_access_keys" {
  for_each = aws_iam_user.users

  user = aws_iam_user.users[each.key].name
}

locals {
  user_names     = keys(aws_iam_user.users)
  last_user_name = local.user_names[length(local.user_names) - 1]
}

output "last_user_credentials" {
  value = {
    name       = aws_iam_user.users[local.last_user_name].name
    access_key = aws_iam_access_key.user_access_keys[local.last_user_name].id
    secret_key = aws_iam_access_key.user_access_keys[local.last_user_name].secret
  }
    sensitive = true
}