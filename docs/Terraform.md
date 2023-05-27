# Configurando a infraestrutura com Terraform

<div style = "text-align: justify">

### Uma das primeiras coisas a se pensar é: Como conectar o Terraform com a AWS?

No seu computador, crie uma pasta com o nome terraform. Nela, faça um *terraform init* no terminal para inicializar o terraform, se a saída for parecida com essa, está tudo ok e o terraform foi inicializado corretamente!

<div style ="display:flex;align-items:center;justify-content:center;"><img src="/image/terraform_init.png"></div>

Nela, pode-se criar um arquivo user_create.tf, que vai ser a estrutura principal para criação de usuários. Para identificar que é o bloco de configuração principal do terraform que vai definir configurações globais para o ambiente de execução, precisa-se utilizar o bloco terraform {} antes de definir recursos e regras específicas do ambiente.

Dentro do bloco terraform, precisa-se colocar a primeira configuração. O bloco required_providers é exatamente o que o nome propõe, ou seja, se define as dependências do provedor necessário para a configuração, conforme apresentado abaixo:

**user_create.tf**
```hcl
terraform {

required_providers {

    aws = {

    source  = "hashicorp/aws" 

    version = "~> 4.67.0" # Versão da AWS maior que 4.67.0

    }
  }
}
```

Agora, definido o provider que será utilizado, é necessário se conectar á uma conta no provedor. Para isso, ainda no arquivo user_create, deve ser adicionado mais um bloco chamado provider, que nele será definido a região e a chave de acesso.

**user_create.tf**
```hcl
provider "aws" {
    region     = "us-east-1"
    access_key = "${var.access_key}"
    secret_key = "${var.secret_key}"
}
```

Nesse código, foi definido a região de Norte da Virgínia, e a access_key e a secret_key do usuário. Porém, de onde está vindo essa var.access_key e var.secret_key? Por motivos de segurança, a access_key e a secret_key não devem estar no arquivo principal do terraform, e sim em um arquivo por fora, ou que esteja sempre no .gitignore. Um arquivo muito conhecido próprio do terraform é o terraform.tfvars, que é um arquivo que nunca deve ir para o git e por padrão deve estar presente .gitignore. Portanto, é necessário criar um arquivo terraform.tfvars conforme explicado abaixo, e nele sim, você coloca sua chave de acesso.

**terraform.tfvars**
```hcl
access_key = "AKIAIOSFODNN7EXAMPLE"
secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
```

::: info
Essa chave acima é apenas um exemplo, não sendo de uma conta real! Novamente, cuide da sua chave de acesso, pois ela é única e não pode ser liberada na internet de forma alguma. Caso perca sua chave, terá que criar um novo par na AWS.
:::

Além do terraform.tfvars, deve-se utilizar mais um arquivo extra para identificar as variáveis e também organizar o projeto. Para isso, deve ser feito mais um arquivo chamado variables.tf, onde nele terá as variáveis usadas no projeto junto com sua descrição.

**variables.tf**
```hcl
variable "access_key" {
    description = "Access key to AWS console"
}
variable "secret_key" {
    description = "Secret key to AWS console"
}
```

Feito esses ajustes, agora temos o Terraform conectado à AWS com o seu provider inicial. Agora, voltando para o arquivo user_create.tf, devemos criar os usuários. O Terraform consegue criar e manter estado de infraestruturas, ou seja, ao criar uma nova estrutura, ele mantém o antigo e cria um novo, e isso funciona exatamente por causa da função for_each. Ela é usada para criar recursos de infraestrutura em massa com base em um mapa ou conjunto de pares-chave. Ela permite iterar sobre os elementos de um mapa ou conjunto e criar uma instância do recurso para cada elemento, por exemplo. No nosso caso, queremos utilizar ela para sempre iterar números de usuários. Existe também a função count que funciona de forma parecida, entretanto, não serve para o problema em questão, pois ela necessita de um número fixo, e o projeto aumenta a quantidade de usuário de acordo com o cliente que utiliza a plataforma no terminal pelo python. 

Nesse sentido, no user_create, adiciona-se o seguinte bloco:

**user_create.tf**
```hcl
resource "aws_iam_user" "users" {
  for_each = var.users

  name = each.value.name
  path = each.value.path
  tags = each.value.tags
}
```

O bloco chamado resource têm seus tipos padrões em relação à AWS, ou seja para criar instância, por exemplo, seria "aws_instance", mais exemplos podem ser vistos aqui: <a href="https://developer.hashicorp.com/terraform/language/resources/syntax" target="_blank">HashiCorp Resource Types Docs</a>. Como queremos utilizar IAM users, o tipo é "aws_iam_user" com o nome local "users".

Como a for_each pode ser usada dentro de um bloco de recurso, e seu argumento é um mapa ou conjunto, cada chave-valor no mapa ou cada elemento no conjunto corresponderá a uma atributo do usuário, que no caso vem de *var.users*. Como já visto anteriormente, esse users é uma variável e ela deve ser definida para o for_each poder buscá-la. Por questão de organização, e pensando no python que será feito mais na frente, é necessário criar um novo arquivo chamado users.tf.

**users.tf**
```hcl
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
```

Nesse arquivo, é definido a variable users como um mapa de objetos, que possui um nome do usuário, o path sendo o caminho que a variável deve seguir no IAM, a policy_arn representando as políticas que o usuário possui, e tags para mais informações sobre o usuário. O default vai servir para guardar e manter os usuários que o cliente vai querer criar. Essa parte que será integrada com o python para poder manter antigos usuários e criar novos usuários. Segue um exemplo de como vai ficar após o cliente adicionar o primeiro usuário pelo python.

**exemplo de users.tf**
```hcl
variable "users" {
  type = map(object({
    name = string
    path = string
    policy_arns = list(string)
    tags = map(string)
  }))
  default = {

	user1 = {
		name = "user1"
		path = "/"
		policy_arns = ["arn:aws:iam::aws:policy/AdministratorAccess"]
		tags = {
			Name = "user1"
	}},
    #ultimo 
  }
}
```

::: warning
Essa linha #ultimo é essencial para funcionamento do python, por favor, não retire ela de forma alguma.
:::

Aprendendo isso, torna muito mais fácil olhar o código do resource aws_iam_user, pois agora dá para notar que cada user que estiver no default do users irá ser criado com os devidos nomes, path e tags. Entretanto, ainda está faltando a política e isso se deve porque a atribuição de políticas funciona de forma mais diferente. Ainda no user_create.tf, deve-se adicionar mais um bloco de resource.

**user_create.tf**
```hcl
resource "aws_iam_user_policy_attachment" "user_policies" {
  for_each = var.users

  user       = aws_iam_user.users[each.key].name
  policy_arn = each.value.policy_arns[0]
}
```

Assim como o próprio nome da resource representa, esse bloco adiciona cada política ao seu respectivo usuário, como no projeto foi escolhido apenas para criar usuários com uma política só, foi utilizado a primeira política da lista, por isso o policy_arns[0]. Mas, caso queira trabalhar com mais políticas, basta adequar o programa em python.

Com isso, temos a base de criação de um usuário. Entretanto, agora temos que pensar como que podemos fazer a criação de um administrador, pois, como administrador, ele poderá criar novos usuários e para isso, vai ser necessário ter suas chave de acesso, então precisamos que o Terraform nos retorne essas informações. Para isso, foi adicionado mais uns blocos de código.

**user_create.tf**
```hcl
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
```
Nesse bloco, além de usarmos o resouce, foi utilizado mais alguns blocos novos. Explicando primeiramente o resource, que foi utilizado o type "aws_iam_access_key" que está criando uma chave de acesso para cada usuário. A partir disso, vai para o segundo bloco "locals", que assim como o nome indica, está criando variáveis locais para ser mais fácil o acesso ás informações. Dentro do locals, a primeira linha funciona para guardar numa lista todas os id's(access_key) de todos os usuários. A partir disso, na segunda linha, nós conseguimos pegar o id do último usuário criado.

Finalmente, no último bloco, é utilizado o bloco "output", que são informações que o Terraform retorna após ter feito toda a aplicação. Dentro do bloco, devido também ás variáveis locais criadas anteriormente, se consegue pegar o nome, o access_key e o secret_key do último usuário criado guardado numa variável chamada last_user_credentials. É necessário colocar o atributo sensitive = true, por ser uma informação valiosa que não pode simplesmente sair no terminal.

Para testar essa infraestrutura sem o programa python, basta apenas usar o exemplo de users.tf em users, e no resto da estrutura não precisa mudar mais nada. Para observar todas as mudanças que serâo feitas, rode no terminal *terraform plan* e para aplicar as mudanças na AWS, rode *terraform apply*. Para retornar para o estado que deve ser iniciado com python, dê um *terraform destroy* e volte o users.tf com apenas a hashtag #ultimo.

Pronto, agora temos toda a infraestrutura do Terraform criada. Porém, para ela ser aplicada como o projeto pede, necessitamos de uma ajuda de um programa python.

</div>
