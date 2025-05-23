from pathlib import Path
import json
import hashlib

path = Path('user.json')

def login(users):
    CPF_ver = input('Bem vindo de volta, informe seu CPF: ')
    Rawpass = input('Digite sua senha: ')
    Rawpass = Rawpass.encode()
    senha_ver = hashlib.sha256(Rawpass).hexdigest()
    for database in users:
        for CPF in database:
            if CPF == CPF_ver and senha_ver == database[CPF]['senha']:                
                print(f'Bem vindo, {database[CPF]["nome_completo"]}!')
                while True:
                    action = input(f'Por favor, digite a ação desejada: SACAR, DEPOSITAR ou EXTRATO. (Digite Q para deslogar): ').upper()
                    if action == 'SACAR':
                        saque(CPF_ver, users)
                    elif action == 'DEPOSITAR':    
                        depositar(CPF_ver, users)
                    elif action == 'EXTRATO':    
                        extrato(CPF_ver, users)    
                    elif action == 'Q':                            
                        print('Encerrando sistema... Até a próxima!')
                        break
                    else:
                        print('Ação desconhecida.')
            else:        
                print('CPF ou senha incorreto. Por favor, verifique os dados inseridos.')

    return CPF_ver   

def cadastro():
    if path.exists():
        brute_info = path.read_text()
        users = json.loads(brute_info)     
        CPF = input('Qual seu CPF?: ')
        usuario = {
                'nome_completo': input('Digite seu nome completo: '),
                'idade': input('Digite sua idade: '),
                'localizacao': input('Digite sua localização: '),
                'senha': input('Crie sua senha: '),
                'saldo': 0
            }
        
        bytes = usuario['senha'].encode()
        usuario['senha'] = hashlib.sha256(bytes).hexdigest()

        database = {CPF: usuario}
        users.append(database)
        content = json.dumps(users)
        path.write_text(content)
         
    ## ESQUEMA DE ARMAZENAMENTO: a lista USERS, armazena o dicionario DATABASE, cuja chave é CPF, cuja armazena o dicionario USUARIO que contem as informações.                
    
    else:    
        CPF = input('Qual seu CPF?: ')
        usuario = {
                'nome_completo': input('Digite seu nome completo: '),
                'idade': input('Digite sua idade: '),
                'localizacao': input('Digite sua localização: '),
                'senha': input('Crie sua senha: '),
                'saldo': int(0)
            }

        bytes = usuario['senha'].encode()
        usuario['senha'] = hashlib.sha256(bytes).hexdigest()

        database = {CPF: usuario}
        users = [database]
        content = json.dumps(users)
        path.write_text(content)    
        
    print('Seu cadastro foi criado com sucesso!')    
    return users
