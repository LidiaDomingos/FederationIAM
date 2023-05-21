variable "users" {
  type = map(object({
    name = string
    path = string
    policy_arns = list(string)
    tags = map(string)
  }))
  default = {

	teste1 = {
		name = "teste1"
		path = "/"
		policy_arns = ["arn:aws:iam::aws:policy/AdministratorAccess"]
		tags = {
			Name = "teste1"
	}},

	teste2 = {
		name = "teste2"
		path = "/"
		policy_arns = ["arn:aws:iam::aws:policy/AdministratorAccess"]
		tags = {
			Name = "teste2"
	}},
    #ultimo 
  }
}
