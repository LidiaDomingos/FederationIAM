# Configurando a infraestrutura com Terraform

<div style = "text-align: justify">

### Uma das primeiras coisas a se pensar é: Como conectar o Terraform com a AWS?

No seu computador, crie uma pasta com o nome terraform. Nela, pode-se criar um arquivo user_create.tf, que vai ser a estrutura principal para criação de usuários. Para identificar que é o bloco de configuração principal do terraform que vai definir configurações globais para o ambiente de execução, precisa-se utilizar o bloco terraform {} antes de definir recursos e regras específicas do ambiente.

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

</div>

Agora, definido o provider que será utilizado, é necessário se conectar á uma conta no provedor. Para isso, ainda no arquivo user_create, adiciona 


## Syntax Highlighting

VitePress provides Syntax Highlighting powered by [Shiki](https://github.com/shikijs/shiki), with additional features like line-highlighting:

**Input**

````
```js{4}
export default {
  data () {
    return {
      msg: 'Highlighted!'
    }
  }
}
```
````

**Output**

```js{4}
export default {
  data () {
    return {
      msg: 'Highlighted!'
    }
  }
}
```

## Custom Containers

**Input**

```md
::: info
This is an info box.
:::

::: tip
This is a tip.
:::

::: warning
This is a warning.
:::

::: danger
This is a dangerous warning.
:::

::: details
This is a details block.
:::
```

**Output**

::: info
This is an info box.
:::

::: tip
This is a tip.
:::

::: warning
This is a warning.
:::

::: danger
This is a dangerous warning.
:::

::: details
This is a details block.
:::

## More

Check out the documentation for the [full list of markdown extensions](https://vitepress.dev/guide/markdown).
