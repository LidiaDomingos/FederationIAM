# Pré-requisitos

<div style = "text-align: justify">

## AWS

Para fazer o projeto, é necessário possuir uma conta na AWS e criar um usuário administrador para ser o usuário padrão. Precisar ter o nome, o access key e o secret key desse usuário padrão. Essas chaves funcionam para permitir o acesso à AWS por fora do dashboard, ou seja, pelo AWS CLI ou pela API da AWS.

Essas credenciais podem ser obtidas por meio do dashboard da AWS, após ter criado o usuário, na aba de credenciais de segurança, conforme ensina o <a href="https://docs.aws.amazon.com/pt_br/powershell/latest/userguide/pstools-appendix-sign-up.html" target="_blank">tutorial próprio</a> da AWS. 

::: danger
Cuidado para não perder a senha, pois, após criada e salva, não será possível recuperá-la. Não compartilhe de forma alguma essas chaves para não ter acesso indesejado na conta da AWS. Não use as credenciais da conta root, mas sim, crie um usuário que simule a conta root.
:::

## Terraform 

Para instalar o Terraform, basta seguir o <a href="https://developer.hashicorp.com/terraform/downloads?ajs_aid=728995f7-4d4f-4fdc-85a1-c3499c02a83f&product_intent=terraform" target="_blank">tutorial próprio</a> da HashiCorp. Escolha a versão de acordo com o seu computador!

## Python

Para instalar o Python, basta seguir o <a href="https://www.python.org/downloads/" target="_blank">tutorial próprio</a> da PythonOrg. Escolha a versão de acordo com o seu computador!

</div>