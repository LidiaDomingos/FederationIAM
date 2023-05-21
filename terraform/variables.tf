variable "access_key" {
    description = "Access key to AWS console"
}
variable "secret_key" {
    description = "Secret key to AWS console"
}

# variable "policy_arns" {
#   default = ["arn:aws:iam::aws:policy/AdministratorAccess"]
#   type        = list(string)
#   description = "ARN of policy to be associated with the created IAM user"
# }
