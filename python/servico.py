import json
import os

loop = True

# Deve ser alterado.
path_terraform = "/mnt/c/Terraform/FederationIAM/terraform"
path_python = "/mnt/c/Terraform/FederationIAM/python"

print("Bem vindo à interface de usuários.")
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