---
outline: deep
---
<div style = "text-align: justify">

# Integrando com Python

Para poder dar essa autonomia para o cliente, é necessário fazer um programa em python. O programa a seguir foi feito baseado na minha arquitetura de pastas e arquivos, e ele permite fazer apenas alguns fluxos de dados, não sendo tudo o que a infraestrutura criada em terraform permite. Partindo do princípio que eu foi criado meu usuário e mais dois usuários administradores, o programa python funciona da seguinte maneira no terminal:

## Fluxo de dados

<div style ="display:flex;align-items:center;justify-content:center;"><img src="/image/FD_1.png"></div>

### Criação de um usuário administrador.

<div style ="display:flex;align-items:center;justify-content:center;"><img src="/image/FD_2.png"></div>

*terraform plan*

<div style ="display:flex;align-items:center;justify-content:center;"><img src="/image/FD_3.png"></div>

*terraform apply*

<div style ="display:flex;align-items:center;justify-content:center;"><img src="/image/FD_4.png"></div>
<div style ="display:flex;align-items:center;justify-content:center;"><img src="/image/FD_5.png"></div>

### Criação de um usuário ReadOnly.

Note que o admin3 agora aparece disponível como um usuário para criar outros usuários.

<div style ="display:flex;align-items:center;justify-content:center;"><img src="/image/FD_6.png"></div>

*terraform plan*

<div style ="display:flex;align-items:center;justify-content:center;"><img src="/image/FD_7.png"></div>

*terraform apply*

<div style ="display:flex;align-items:center;justify-content:center;"><img src="/image/FD_8.png"></div>

Criamos um usuário e criamos outro usuário a partir do que foi o último criado! É importante comentar que, como o usuário criado tem permissões ReadOnly, ele não aparece como uma opção para criar mais usuários, conforme indica figura abaixo:

<div style ="display:flex;align-items:center;justify-content:center;"><img src="/image/FD_9.png"></div>

Você pode observar as mudanças feitas no próprio dashboard da AWS:

<div style ="display:flex;align-items:center;justify-content:center;"><img src="/image/FD_10.png"></div>

## Como o programa funciona?

Esse programa em python se interliga com o Terraform de várias formas. O Python foi criado já pensando em como integrar com o Terraform, por isso, tem alguns pontos que são essenciais para o funcionamento do programa. Podemos dividir o Python em blocos para poder explicar com clareza o fluxo de dados que ocorre. Além disso, é necessário seguir a mesma organização de arquivos e pastas se quiser utilizar esse arquivo pronto. Mas também pode refatorar o python para o seu desejo, como por exemplo, de adicionar mais de uma política para um usuário só. Segue o código completo a seguir:

**servico.py**
```python
import json
import os

loop = True

# Deve ser alterado.
path_terraform = "/mnt/c/Terraform/FederationIAM/terraform"
path_python = "/mnt/c/Terraform/FederationIAM/python"

print("\nBem vindo à interface de usuários.")
print("----------------------------------")
print("Inicializando o Terraform!")
print("----------------------------------\n")

os.chdir(path_terraform)
os.system("terraform init")

policy_admin = '["arn:aws:iam::aws:policy/AdministratorAccess"]'
policy_readOnly = '["arn:aws:iam::aws:policy/IAMReadOnlyAccess"]'

while loop:
    resposta = input("\nVocê deseja adicionar um novo usuário?(S/N)\n")
    if resposta == "S" or resposta == "s":

        print("\nUsuários disponíveis na AWS:\n")
        os.chdir(path_python)

        f = open('credentials.json')
        data = json.load(f)
        count_index = 0
        for indice, dic in data.items():
            print(f'{count_index}. {dic["name"]}')
            count_index+=1
        f.close()

        index = input("\nA partir de qual usuário você deseja criar? Digite aqui o índice: \n")
        for key, value in data.items():
            if int(key) == int(index):
                os.chdir(path_terraform)
                with open('terraform.tfvars', 'r') as file:
                    lines = file.readlines()
                for i, line in enumerate(lines):
                    if line.startswith('access_key' + ' = '):
                        lines[i] = 'access_key' + ' = ' + f'"{value["access_key"]}"' +'\n' 
                    elif line.startswith('secret_key' + ' = '):
                        lines[i] = 'secret_key' + ' = ' + f'"{value["secret_key"]}"' + '\n'
                file.close()

                with open('terraform.tfvars', 'w') as file:
                    file.writelines(lines)
                file.close()

        policy = input("\nQual política você deseja fornecer ao usuário?\n\n\t1. Administrator Access: Essa política concede permissões de administrador completo para todos os serviços e recursos da AWS.\n\t2. IAM Read Only Access: Essa política fornece somente permissões de leitura para visualizar recursos e configurações do IAM, não sendo possível fazer alterações, ou seja, esse usuário não consegue criar outros usuários.\n\n Digite aqui o índice da política desejada: \n")
        nome = input("\nDigite aqui o nome do novo usuário: \n")
        lista = []

        with open('users.tf', 'r') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                lista.append(line)
        file.close()

        for i in range(0, len(lista)):
            if "#" in lista[i]:
                if policy == '1':
                    chosen = policy_admin
                else:
                    chosen = policy_readOnly 
                lista.insert(i, "\t}},\n")
                lista.insert(i,'\t\t\tName' + ' = ' + f'"{nome}"' + "\n" )
                lista.insert(i, '\t\ttags = {\n')
                lista.insert(i, f'\t\tpolicy_arns = {chosen}\n')
                lista.insert(i,'\t\tpath = "/"\n')
                lista.insert(i,'\t\tname' + ' = ' + f'"{nome}"' + "\n" )
                lista.insert(i,"\n\t" + f'{nome}' + ' = ' + '{\n')

        with open('users.tf', "w") as f:
            f.writelines(lista)
        f.close()
        
        os.system("terraform plan")
        os.system("terraform apply")
        os.system("terraform output -json last_user_credentials > last_credential.json")
        
        if policy == '1':
            last_credential = json.load(open('last_credential.json'))
            os.chdir(path_python)
            dic = json.load(open('credentials.json'))
            novo_dic = {}
            dic2 = {}
            novo_dic[str(len(dic))] = {}
            dic2["name"] = last_credential["name"]
            dic2["access_key"] = last_credential["access_key"]
            dic2["secret_key"] = last_credential["secret_key"]
            novo_dic[str(len(dic))] = dic2
            dic.update(novo_dic)

            with open("credentials.json", 'w') as file:
                json.dump(dic, file, indent = 2)
                
            file.close()

    elif resposta == "N" or resposta == "n":
        print("----------------------------------")
        print("Tenha um bom dia!")
        loop = False
    else:
        print("Por favor, digite uma resposta válida!")
```
## Pontos mais importantes a se considerar:

### 1. Caminho:

**servico.py**
```python
path_terraform = "/mnt/c/Terraform/FederationIAM/terraform"
path_python = "/mnt/c/Terraform/FederationIAM/python"
```

Como o projeto foi dividido em duas pastas, é necessário o python buscar de pasta em pasta os arquivos que ele vai usar, então eu defino o caminho das pastas nessas duas variáveis. Troque para o caminho existente no seu computador.

### 2. Políticas escolhidas:

```python
policy_admin = '["arn:aws:iam::aws:policy/AdministratorAccess"]'
policy_readOnly = '["arn:aws:iam::aws:policy/IAMReadOnlyAccess"]'
```

As políticas escolhidas para o escopo do projeto foram essas, mas você também pode alterar para alguma outra que você deseja, mas lembre-se de alterar o resto do python para suprir essa necessidade.

### 3. Usuários já existentes:

```python
print("\nUsuários disponíveis na AWS:\n")
os.chdir(path_python)
f = open('credentials.json')
```

Uma forma que foi pensada em como conseguir os usuários já existentes foi-se criando um credentials.json na pasta python, onde nele teria um usuário administrador base, com o nome do usuário, sua access_key e sua secret_key, para começar a federação de usuários, sendo um jeito de conseguir buscar usuários e suas chaves, já que a AWS só retorna essa chave uma única vez. Essa não é a melhor forma de guardar esses usuários e suas chaves, sendo o ideal guardar em um vault, porém, como o projeto visa apenas demonstrar um escopo do que seria o ideal, foi utilizado um json como um banco de dados. Segue abaixo o exemplo usado no fluxo de dados acima e como as credentials estavam inicialmente.

**credentials.json**
```json
{
  "0": {
    "name": "lidia",
    "access_key": "AKIAIOSFODNN7EXAMPLE",
    "secret_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
  },
  "1": {
    "name": "admin1",
    "access_key": "AKIAIOSFODNN7EXAMPLE",
    "secret_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
  },
  "2": {
    "name": "admin2",
    "access_key": "AKIAIOSFODNN7EXAMPLE",
    "secret_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
  },
}
```

::: info
Novamente, essas chaves acima são apenas um exemplo! Cuide da sua chave de acesso, pois ela é única e não pode ser liberada na internet de forma alguma. Caso você queira fazer esse projeto e melhorar, esse arquivo é essencial que esteja no .gitignore, para não liberar de forma alguma na internet.
:::

Observando o fluxo de dados acima, após a criação do novo usuário administrador no terminal, o programa python reescreve esse json com o novo usuário, conforme indica essa parte do código:

```python
os.system("terraform output -json last_user_credentials > last_credential.json")

if policy == '1':
    last_credential = json.load(open('last_credential.json'))
    os.chdir(path_python)
    dic = json.load(open('credentials.json'))
    novo_dic = {}
    dic2 = {}
    novo_dic[str(len(dic))] = {}
    dic2["name"] = last_credential["name"]
    dic2["access_key"] = last_credential["access_key"]
    dic2["secret_key"] = last_credential["secret_key"]
    novo_dic[str(len(dic))] = dic2
    dic.update(novo_dic)

    with open("credentials.json", 'w') as file:
        json.dump(dic, file, indent = 2)
        
    file.close()
```
::: tip
O que é esse "terraform output -json last_user_credentials > last_credential.json"?
Bom, ele é um comando especial do terraform que colocar a variável local, ou seja, o last_user_credentials em um json chamado last_credential na pasta terraform, onde o python irá ler, e caso a política do usuário for Administrador, irá adicionar no credentials.json!
::: 

Após esse código, o credentials.json passa a ficar assim, e por isso, o admin3 aparece como um usuário possível de criar:

**credentials.json pós a criação do usuário admin3**
```json
{
  "0": {
    "name": "lidia",
    "access_key": "AKIAIOSFODNN7EXAMPLE",
    "secret_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
  },
  "1": {
    "name": "admin1",
    "access_key": "AKIAIOSFODNN7EXAMPLE",
    "secret_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
  },
  "2": {
    "name": "admin2",
    "access_key": "AKIAIOSFODNN7EXAMPLE",
    "secret_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
  },
  "3": {
    "name": "admin3",
    "access_key": "AKIAIOSFODNN7EXAMPLE",
    "secret_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
  }
}
```
### 4. Definir o usuário provider que vai criar o novo usuário

Assim como já falado anteriormente, é necessário que a AWS tenha um provider para criar seu novo usuário e que esse provider seja o que o usuário escolha. Entenda o código a seguir:

```python
index = input("\nA partir de qual usuário você deseja criar? Digite aqui o índice: \n")
for key, value in data.items():
    if int(key) == int(index):
        os.chdir(path_terraform)
        with open('terraform.tfvars', 'r') as file:
            lines = file.readlines()
        for i, line in enumerate(lines):
            if line.startswith('access_key' + ' = '):
                lines[i] = 'access_key' + ' = ' + f'"{value["access_key"]}"' +'\n' 
            elif line.startswith('secret_key' + ' = '):
                lines[i] = 'secret_key' + ' = ' + f'"{value["secret_key"]}"' + '\n'
        file.close()

        with open('terraform.tfvars', 'w') as file:
            file.writelines(lines)
        file.close()
```

Ele abre o arquivo terraform.tfvars e altera o id e a secret_key para a chave do usuário escolhido pelo cliente.

### 5. Adicionar usuários no users.tf

Após definido todos os atributos do usuário, é necessário passar esse usuário para o users.tf, para assim o terraform ir criando esses novos usuários. Observe a código a seguir:

```python
with open('users.tf', 'r') as file:
    lines = file.readlines()
    for i, line in enumerate(lines):
        lista.append(line)
    file.close()

    for i in range(0, len(lista)):
        if "#" in lista[i]:
            if policy == '1':
                chosen = policy_admin
            else:
                chosen = policy_readOnly 
            lista.insert(i, "\t}},\n")
            lista.insert(i,'\t\t\tName' + ' = ' + f'"{nome}"' + "\n" )
            lista.insert(i, '\t\ttags = {\n')
            lista.insert(i, f'\t\tpolicy_arns = {chosen}\n')
            lista.insert(i,'\t\tpath = "/"\n')
            lista.insert(i,'\t\tname' + ' = ' + f'"{nome}"' + "\n" )
            lista.insert(i,"\n\t" + f'{nome}' + ' = ' + '{\n')

    with open('users.tf', "w") as f:
        f.writelines(lista)
    f.close()
```

Essa parte do código lê o arquivo users.tf, e reescreve ele adicionando o usuário definido, conforme já apresentado na página de Terraform anterior, é por isso também que não se pode tirar a linha "#ultimo" e nem colocar comentário nessa parte, pois foi como identificar onde adicionar no json esse novo usuário.
 
::: warning
Note que o python não possui tratamento para caso o cliente não digite o que é esperado, então, por favor, digite apenas entradas válidas para não quebrar o programa.
:::

::: tip
Se for utilizar esse projeto e for colocar no git, lembre-se de utilizar o .gitignore com pelo menos essas restrições:
*.tfstate
*.tfvars
*.tfvars.json
*.json . Não libere de forma alguma suas senhas na internet!
:::
Agora sim, tendo tudo isso definido, basta abrir o terminal na pasta python e digitar "python3 service.py", ou com o python que você tiver disponível, e se divertir 😃.

</div>