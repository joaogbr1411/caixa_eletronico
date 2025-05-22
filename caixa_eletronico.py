from pathlib import Path
import json
import hashlib

path = Path('user.json')

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