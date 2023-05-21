variable "users" {
  type = map(object({
    name = string
    path = string
    policy_arns = list(string)
    tags = map(string)
  }))
  default = {
    #ultimo 
  }
}
