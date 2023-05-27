# Uma visão geral

<div style = "text-align: justify">

## O que é computação em nuvem?

A computação em nuvem é um modelo de fornecimento de serviços de computação por meio da internet. Ela permite acesso e uso remoto de recursos computacionais como servidores, armazenamento e software. Isso ajuda bastante no sentido de não ser necessário a pessoa estar em um computador local/servidor físico para poder fazer seu trabalho, e ter essa praticidade e agilidade de acesso em qualquer local do mundo.

Além disso, torna muito mais fácil o acesso á estruturas computacionais sem necessariamente ter que montar toda a estrutura fisíca que um servidor necessita, ou mesmo um data center, podendo apenas contratar um provedor, para ter acesso à armazenamento e milhares de servidores, além de diversos serviços próprios que cada provedor oferece. 

<div style ="display:flex;align-items:center;justify-content:center;"><img src="/image/what-is-the-cloud.png"></div>

Um dos provedores mais famosos é a Amazon Web Services (AWS), que é exatamente o servioço que vai ser utilizado no projeto. Mais especificamente, a parte de usuários da AWS.

## O que é IAM?

O AWS Identity and Access Management (IAM) é um dos diversos serviços que a Amazon disponibiliza e um dos mais importantes para o próprio funcionamento de todos os outros serviços da AWS. Afinal, para conseguir desenvolver qualquer projeto, é necessário ter um usuário por trás que tenha permissão para utilizar uma tal ferramenta.

A partir do momento que você cria uma conta na AWS, você pode acessar o dashboard utilizando um usuário root (endereço de email) com todas as permissões adquiridas na hora da compra. Entretanto, tendo uma visão mais de mercado de trabalho, onde podem se ter diversas pessoas que devem ter acesso ao dashboard para fazerem suas tarefas, esse usuário não pode ser o mesmo para todo mundo.

O IAM cuida exatamente disso. Na AWS, você pode criar vários usuários com diferentes permissões, e assim ter um controle muito maior do que cada usuário pode fazer. 

## O que é Terraform?

O Terraform é uma ferramenta de infraestrutura como código que permite definir e gerenciar recursos de computação de forma declarativa. Basta escrever arquivos de configuração descrevendo a infraestrutura necessária e o Terraform se encarrega de criar esse estado. Ele oferece suporte a vários provedores de infraestrutura, inclusive a AWS, e trata a infraestrutura como código, permitindo controle de versão, colaboração e automação de provisionamento. Isso garante consistência e repetibilidade no desenvolvimento e implantação de aplicativos.

Com essa aplicação, se torna possível transformar o fluxo de dados que seria feito no dashboard da AWS para código, podendo repetir uma infraestrutura de forma muito mais prática e ágil.

## O que isso significa no contexto do projeto?

A ideia desse roteiro é exatamente automatizar essa criação e atribuição de permissões na AWS de uma forma simplificada e somente a partir do terminal para um usuário root, ou seja, que controle todos os outros usuários, conforme ilustra a imagem a seguir:

<div style ="display:flex;align-items:center;justify-content:center;"><img src="/image/img_exemplo.svg"></div>

Ou seja, por meio da interface no terminal criada com Python, os arquivos de Terraform são alterados de acordo com o que o cliente que utiliza o serviço do terminal necessita e digita. 

</div>