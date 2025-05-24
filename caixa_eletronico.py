from pathlib import Path
import json
import hashlib
import smtplib
from email.message import EmailMessage

path = Path('user.json')

##verifica cada dicionario em busca do CPF correspondente e da boas vindas ao nome do mesmo
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

        msg = EmailMessage() ##cria objeto da classe message
        msg['From'] = 'sobek0955@gmail.com'
        msg['To'] = usuario['email']
        msg['Subject'] = 'Sua conta foi criada com sucesso!'
        corpo = f"Olá, {usuario['nome_completo'].title()}! Sua conta foi criada com sucesso. Realize seu primeiro depósito e inicie suas movimentações, obrigado pela confiança!"
        msg.set_content(corpo)

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls() #Ativa criptografia TLS na conexão
            smtp.login('sobek0955@gmail.com', 'ltngjmqxmtqbxevc')
            smtp.send_message(msg)    
        
        print('Seu cadastro foi criado com sucesso!')    
        return users
         
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

        msg = EmailMessage() ##cria objeto da classe message
        msg['From'] = 'sobek0955@gmail.com' ##define remetente
        msg['To'] = usuario['email'] ##define destinatario
        msg['Subject'] = 'Sua conta foi criada com sucesso!' #define o assunto
        corpo = f"Olá, {usuario['nome_completo'].title()}! Sua conta foi criada com sucesso. Realize seu primeiro depósito e inicie suas movimentações, obrigado pela confiança!" #criação do corpo
        msg.set_content(corpo) #define o corpo

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp: ##conecta com o servidor SMPT do gmail
            smtp.starttls() ##ativa o protocolo de criptografia TLS
            smtp.login('sobek0955@gmail.com', 'ltngjmqxmtqbxevc') ##conecta coom o remetente
            smtp.send_message(msg) ## envia a mensagem    
        
        print('Seu cadastro foi criado com sucesso!')    
        return users    
        

def depositar(CPF_ver, users):
    dep_valor = int(input('Digite a quantia a ser depositada: '))
    for database in users:
        for CPF in database:
            if CPF == CPF_ver:
                database[CPF]["saldo"] = database[CPF]["saldo"] + dep_valor
                content = json.dumps(users)
                path.write_text(content) 
                print(f'{dep_valor} foi depositado com sucesso!')

def saque(CPF_ver, users):
    saque = int(input('Digite a quantia para ser sacada: '))
    for database in users:
        for CPF in database:
            if CPF == CPF_ver:
                database[CPF]["saldo"] = database[CPF]["saldo"] - saque
                content = json.dumps(users)
                path.write_text(content) 
                print(f'{saque} foi sacado com sucesso!')

def extrato(CPF_ver, users):
    for database in users:
        for CPF in database:
            if CPF == CPF_ver:
                print(f'Seu saldo é {database[CPF]['saldo']}')


initial_ver = input('Você já possui uma conta? Digite SIM ou NAO: ').upper() #INICIO DO CÓDIGO
if initial_ver == 'NAO':
    cadastro()

if initial_ver == 'SIM':   
    info = path.read_text() #CAPTURA AS INFORMAÇÕES
    users = json.loads(info)
    login(users)
