import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import json
import hashlib
import smtplib
from email.message import EmailMessage
import random

path = Path('user.json')
if path.exists():
    brute_info = path.read_text()
    users = json.loads(brute_info)

root = tk.Tk() 
root.title('Simulador de Caixa Eletrônico') 
root.geometry('450x380') 
root.resizable(False, False) 


DEFAULT_FONT = ('Arial', 12)
HEADER_FONT = ('Arial', 16, 'bold')
BUTTON_FONT = ('Arial', 10, 'bold')
ENTRY_WIDTH = 30 


tk.Label(root, text="Simulador de caixa eletrônico", font=("Arial", 18, "bold")).pack(pady=10) 

cpf_label = tk.Label(root, text="CPF:", font=DEFAULT_FONT) 
cpf_label.pack(pady=(20, 5)) 
cpf_entry = tk.Entry(root, font=DEFAULT_FONT, width=ENTRY_WIDTH) 
cpf_entry.pack(pady=5)

senha_label = tk.Label(root, text="Senha:", font=DEFAULT_FONT) 
senha_label.pack(pady=5)
senha_entry = tk.Entry(root, show="*", font=DEFAULT_FONT, width=ENTRY_WIDTH) 
senha_entry.pack(pady=5)

def cadastro_tela():
    limpar_tela() #

    global cpf_criar, nome_criar, idade_criar, email_criar, senha_criar

    tk.Label(root, text="Preencha seus dados para cadastro", font=HEADER_FONT).pack(pady=15)

    text1 = tk.Label(root, text="Insira seu CPF: ", font=DEFAULT_FONT)
    text1.pack(pady=2)
    cpf_criar = tk.Entry(root, font=DEFAULT_FONT, width=ENTRY_WIDTH)
    cpf_criar.pack(pady=2)

    text2 = tk.Label(root, text="Insira seu nome completo:", font=DEFAULT_FONT)
    text2.pack(pady=2)
    nome_criar = tk.Entry(root, font=DEFAULT_FONT, width=ENTRY_WIDTH)
    nome_criar.pack(pady=2)

    text3 = tk.Label(root, text="Insira sua idade: ", font=DEFAULT_FONT)
    text3.pack(pady=2)
    idade_criar = tk.Entry(root, font=DEFAULT_FONT, width=ENTRY_WIDTH)
    idade_criar.pack(pady=2)

    text4 = tk.Label(root, text="Insira seu e-mail: ", font=DEFAULT_FONT)
    text4.pack(pady=2)
    email_criar = tk.Entry(root, font=DEFAULT_FONT, width=ENTRY_WIDTH)
    email_criar.pack(pady=2)

    text5 = tk.Label(root, text="Crie sua senha: ", font=DEFAULT_FONT)
    text5.pack(pady=2)
    senha_criar = tk.Entry(root, show="*", font=DEFAULT_FONT, width=ENTRY_WIDTH)
    senha_criar.pack(pady=2)

    cadastrar_se = tk.Button(root, text="Cadastrar-se", command=cadastrar, font=BUTTON_FONT, width=20, height=2, bg='green', fg='white')
    cadastrar_se.pack(pady=15)

def ver_login():
    cpf = cpf_entry.get()
    senha = senha_entry.get()

    try: 
        brute_info = path.read_text()
        users = json.loads(brute_info)
    except FileNotFoundError:
        messagebox.showerror("Erro de Login", "Arquivo de usuários não encontrado.")
        return
    except json.JSONDecodeError:
        messagebox.showerror("Erro de Login", "Erro ao ler dados de usuários. Arquivo JSON corrompido.")
        return
    except Exception as e:
        messagebox.showerror("Erro de Login", f"Ocorreu um erro inesperado: {e}")
        return

    senha = senha.encode()
    senha = hashlib.sha256(senha).hexdigest()

    found = False
    for database in users:
        for CPF in database:
            if CPF == cpf and senha == database[CPF]['senha']:
                limpar_tela()
                menu_usuario(cpf, users)
                found = True
                break
        if found:
            break

    if not found: 
        messagebox.showerror("Erro de Login", "CPF ou senha incorretos.")

    return cpf


def menu_usuario(cpf, users): 
    limpar_tela()
    for database in users:
        for CPF in database:
            if CPF == cpf:
                welcome_label = tk.Label(root, text=f"Bem vindo, {database[CPF]['nome_completo']}!", font=HEADER_FONT)
                welcome_label.pack(pady=20)
                saldo = tk.Label(root, text=f'Seu saldo atual: R$ {database[CPF]['saldo']:.2f}', font=DEFAULT_FONT)
                saldo.pack(pady=10)

               
                button_frame = tk.Frame(root)
                button_frame.pack(pady=10)

                saque = tk.Button(button_frame, text="Saque", command=lambda: sacar(cpf, users), font=BUTTON_FONT, width=12, height=2)
                saque.pack(side=tk.LEFT, padx=10)

                deposito = tk.Button(button_frame, text="Depósito", command=lambda: depositar(cpf, users), font=BUTTON_FONT, width=12, height=2)
                deposito.pack(side=tk.RIGHT, padx=10)

                tk.Button(root, text="Sair", command=tela_inicial, font=BUTTON_FONT, width=20, height=2, bg='red', fg='white').pack(pady=20)

def cadastro():
    limpar_tela()
    cadastro_tela()

def cadastrar():
    if path.exists():
        try: 
            brute_info = path.read_text()
            users = json.loads(brute_info)
        except json.JSONDecodeError:
            messagebox.showerror("Erro de Cadastro", "Erro ao ler dados de usuários. Arquivo JSON corrompido.")
            return
        except Exception as e:
            messagebox.showerror("Erro de Cadastro", f"Ocorreu um erro inesperado ao carregar usuários: {e}")
            return

        CPF = cpf_criar.get()
        usuario = {
                'nome_completo': nome_criar.get(),
                'idade': idade_criar.get(),
                'email': email_criar.get(),
                'senha': senha_criar.get(),
                'saldo': int(0)
            }

        
        for database in users:
            for CPF_db in database: #
                if CPF_db == CPF:
                    messagebox.showerror("Erro", "CPF já cadastrado. Por favor, insira um CPF não utilizado. Caso seu CPF tenha sido indevidamente cadastrado, entre em contato com nosso suporte.")
                    cadastro_tela()
                    return

        bytes_senha = usuario['senha'].encode() 
        usuario['senha'] = hashlib.sha256(bytes_senha).hexdigest()

        database_new_user = {CPF: usuario} 
        users.append(database_new_user)

        try: 
            content = json.dumps(users)
            path.write_text(content)
        except Exception as e:
            messagebox.showerror("Erro de Cadastro", f"Erro ao salvar dados do novo usuário: {e}")
            return

        bem_vindo(usuario)

        msg = tk.Label(root, text="Seu cadastro foi concluído com sucesso!", fg="green")
        msg.pack()

       

        try: 
            with open("user.json", "w") as file: 
                json.dump(users, file, indent=4)
        except Exception as e:
            messagebox.showerror("Erro de Cadastro", f"Erro ao salvar dados do novo usuário: {e}")
            return

        menu_usuario(CPF, users)

        return users

    else: 
        CPF = cpf_criar.get()
        usuario = {
                'nome_completo': nome_criar.get(),
                'idade': idade_criar.get(),
                'email': email_criar.get(),
                'senha': senha_criar.get(),
                'saldo': int(0)
            }

        bytes_senha = usuario['senha'].encode() 
        usuario['senha'] = hashlib.sha256(bytes_senha).hexdigest()

        database_new_user = {CPF: usuario} 
        users = [database_new_user] 

        try: 
            content = json.dumps(users)
            path.write_text(content)
        except Exception as e:
            messagebox.showerror("Erro de Cadastro", f"Erro ao criar arquivo de usuários: {e}")
            return


        bem_vindo(usuario)

        msg = tk.Label(root, text="Seu cadastro foi concluído com sucesso!", fg="green")
        msg.pack()

       

        try: 
            with open("user.json", "w") as file: 
                json.dump(users, file, indent=4)
        except Exception as e:
            messagebox.showerror("Erro de Cadastro", f"Erro ao salvar dados do novo usuário: {e}")
            return

        menu_usuario(CPF, users) 

        return users

def bem_vindo(usuario):
    msg = EmailMessage() 
    msg['From'] = 'sobek0955@gmail.com' 
    msg['To'] = usuario['email']
    msg['Subject'] = 'Sua conta foi criada com sucesso!'
    corpo = f"Olá, {usuario['nome_completo'].title()}! Sua conta foi criada com sucesso. Realize seu primeiro depósito e inicie suas movimentações, obrigado pela confiança!"
    msg.set_content(corpo)

    try: 
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.starttls() 
                smtp.login('sobek0955@gmail.com', 'ltngjmqxmtqbxevc')
                smtp.send_message(msg)
    except Exception as e:
        messagebox.showwarning("Erro de E-mail", f"Não foi possível enviar o e-mail de boas-vindas: {e}")

def redefinir_E1():
    limpar_tela()

    tk.Label(root, text="Redefinir Senha", font=HEADER_FONT).pack(pady=20)
    tk.Label(root, text="Insira o CPF da sua conta:", font=DEFAULT_FONT).pack(pady=5)
    entry = tk.Entry(root, font=DEFAULT_FONT, width=ENTRY_WIDTH)
    entry.pack(pady=5)

    def avancar():
        CPF_vf = entry.get()
        redefinir_E2(CPF_vf)

    tk.Button(root, text="Avançar", command=avancar, font=BUTTON_FONT, width=15, height=2).pack(pady=15)
    tk.Button(root, text="Voltar", command=tela_inicial, font=BUTTON_FONT, width=15, height=2).pack(pady=5)

def redefinir_E2(CPF_vf):
    try: 
        brute_info = path.read_text()
        users_local = json.loads(brute_info) 
    except FileNotFoundError:
        messagebox.showerror("Erro", "Arquivo de usuários não encontrado.")
        return
    except json.JSONDecodeError:
        messagebox.showerror("Erro", "Erro ao ler dados de usuários. Arquivo JSON corrompido.")
        return
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro inesperado ao carregar usuários: {e}")
        return

    found_user = False
    target_email = None
    for database in users_local:
        for CPF in database:
            if CPF_vf == CPF:
                target_email = database[CPF]['email']
                found_user = True
                break
        if found_user:
            break

    if not found_user:
        messagebox.showerror("Erro", "CPF não encontrado.")
        return

    num = random.randint(100000, 999999)
    email = target_email

    msg = EmailMessage()
    msg['From'] = 'sobek0955@gmail.com'
    msg['To'] = email
    msg['Subject'] = 'Recuperação da senha'
    msg.set_content(
        f'Recebemos uma solicitação para redefinir sua senha. '
        f'Para confirmar, insira este código no programa: {num}'
    )

    try: 
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login('sobek0955@gmail.com', 'ltngjmqxmtqbxevc')
            smtp.send_message(msg)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao enviar email de verificação: {e}")
        return

    
    limpar_tela()

    tk.Label(root, text="Redefinir Senha - Verificação", font=HEADER_FONT).pack(pady=20)
    tk.Label(root, text="Código de verificação:", font=DEFAULT_FONT).pack(pady=5)
    entry_codigo = tk.Entry(root, font=DEFAULT_FONT, width=ENTRY_WIDTH)
    entry_codigo.pack(pady=5)

    tk.Label(root, text="Nova senha:", font=DEFAULT_FONT).pack(pady=5)
    entry_senha = tk.Entry(root, show="*", font=DEFAULT_FONT, width=ENTRY_WIDTH)
    entry_senha.pack(pady=5)

    def concluir():
        num_vf = entry_codigo.get()
        nova_senha = entry_senha.get()
        redefinir_E3(CPF_vf, num, num_vf, nova_senha)

    tk.Button(root, text="Concluir", command=concluir, font=BUTTON_FONT, width=15, height=2).pack(pady=15)
    tk.Button(root, text="Voltar", command=lambda: redefinir_E1(), font=BUTTON_FONT, width=15, height=2).pack(pady=5)
    return

def redefinir_E3(CPF_vf, num, num_vf, nova_senha):
    if num_vf == str(num):
        
        global users 
        found = False
        for database in users:
            for CPF in database:
                if CPF == CPF_vf:
                    database[CPF]['senha'] = nova_senha
                    bytes_senha = database[CPF]['senha'].encode() 
                    database[CPF]['senha'] = hashlib.sha256(bytes_senha).hexdigest()
                    found = True
                    break
            if found:
                break

        if found:
            try: 
                content = json.dumps(users)
                path.write_text(content)
                messagebox.showinfo("Sucesso", "Sua senha foi redefinida com sucesso!")
                tela_inicial()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar a nova senha: {e}")
        else:
            messagebox.showerror("Erro", "Erro interno: CPF não encontrado durante a redefinição.")

            tela_inicial()
    else:
        messagebox.showerror("Erro", "Código de verificação incorreto.")

login_botao = tk.Button(root, text="Login", command=ver_login, font=BUTTON_FONT, width=15, height=2)
login_botao.pack(pady=10)

cadastro_botao = tk.Button(root, text="Cadastrar-se", command=cadastro, font=BUTTON_FONT, width=15, height=2)
cadastro_botao.pack(pady=5)

redefinir_botao = tk.Button(root, text="Esqueceu sua senha?", command=redefinir_E1, font=BUTTON_FONT, width=20, height=1)
redefinir_botao.pack(pady=5)

def tela_inicial():
    limpar_tela()

    tk.Label(root, text="Simulador de caixa eletrônico", font=("Arial", 18, "bold")).pack(pady=10) 

    cpf_label = tk.Label(root, text="CPF:", font=DEFAULT_FONT) 
    cpf_label.pack(pady=(20, 5))
    global cpf_entry 
    cpf_entry = tk.Entry(root, font=DEFAULT_FONT, width=ENTRY_WIDTH) 
    cpf_entry.pack(pady=5)

    senha_label = tk.Label(root, text="Senha:", font=DEFAULT_FONT) 
    senha_label.pack(pady=5)
    global senha_entry 
    senha_entry = tk.Entry(root, show="*", font=DEFAULT_FONT, width=ENTRY_WIDTH) 
    senha_entry.pack(pady=5)

    login_botao = tk.Button(root, text="Login", command=ver_login, font=BUTTON_FONT, width=15, height=2)
    login_botao.pack(pady=10)

    cadastro_botao = tk.Button(root, text="Cadastrar-se", command=cadastro, font=BUTTON_FONT, width=15, height=2)
    cadastro_botao.pack(pady=5)

    redefinir_botao = tk.Button(root, text="Esqueceu sua senha?", command=redefinir_E1, font=BUTTON_FONT, width=20, height=1)
    redefinir_botao.pack(pady=5)


def depositar(cpf, users):
    limpar_tela()
    tk.Label(root, text="Realizar Depósito", font=HEADER_FONT).pack(pady=20)
    tk.Label(root, text="Digite a quantia a ser depositada no campo abaixo:", font=DEFAULT_FONT).pack(pady=5)
    dep_entry = tk.Entry(root, font=DEFAULT_FONT, width=ENTRY_WIDTH)
    dep_entry.pack(pady=5)

   
    action_frame = tk.Frame(root)
    action_frame.pack(pady=15)

    
    def depositar2(cpf_local, users_local): 
        dep_valor_str = dep_entry.get()
        try:
            dep_valor = int(dep_valor_str)
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido. Por favor, insira um número inteiro para o depósito.")
            return

        if dep_valor <= 0: 
            messagebox.showerror("Erro", "Valor inválido. Por favor, insira um número inteiro maior que 0 para o depósito.")
            return

        user_found_deposit = False
        for database in users_local:
            if cpf_local in database:
                database[cpf_local]["saldo"] += dep_valor
                user_found_deposit = True
                break
        
        if user_found_deposit:
            try: 
                content = json.dumps(users_local)
                path.write_text(content)
                messagebox.showinfo("Sucesso", f'Depósito de R$ {dep_valor:.2f} realizado com sucesso.')
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar depósito: {e}")
                return
            menu_usuario(cpf_local, users_local) 
        else:
            messagebox.showerror("Erro", "Usuário não encontrado.") 

    confirm = tk.Button(action_frame, text="Confirmar", command=lambda: depositar2(cpf, users), font=BUTTON_FONT, width=12, height=2)
    confirm.pack(side=tk.LEFT, padx=10)
    tk.Button(action_frame, text="Voltar ao Menu", command=lambda: menu_usuario(cpf, users), font=BUTTON_FONT, width=15, height=2).pack(side=tk.RIGHT, padx=10)


def sacar(cpf, users):
    limpar_tela()
    tk.Label(root, text="Realizar Saque", font=HEADER_FONT).pack(pady=20)
    tk.Label(root, text="Digite a quantia a ser sacada no campo abaixo:", font=DEFAULT_FONT).pack(pady=5)
    saque_entry = tk.Entry(root, font=DEFAULT_FONT, width=ENTRY_WIDTH)
    saque_entry.pack(pady=5)

    
    action_frame = tk.Frame(root)
    action_frame.pack(pady=15)

    
    def sacar2(cpf_local, users_local): 
        saque_valor_str = saque_entry.get()
        try: 
            saque_valor = int(saque_valor_str)
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido. Por favor, insira um número inteiro para o saque.")
            return
        
        if saque_valor <= 0: 
            messagebox.showerror("Erro", "Valor de saque inválido. Insira um valor maior que zero.")
            return

        user_found_sacar = False
        for database in users_local:
            if cpf_local in database:
                user_found_sacar = True
                if database[cpf_local]['saldo'] >= saque_valor:
                    database[cpf_local]['saldo'] -= saque_valor
                    try: #
                        content = json.dumps(users_local)
                        path.write_text(content)
                        messagebox.showinfo("Sucesso", f'Saque de R$ {saque_valor:.2f} realizado com sucesso.')
                    except Exception as e:
                        messagebox.showerror("Erro", f"Erro ao salvar saque: {e}")
                        return
                    menu_usuario(cpf_local, users_local) 
                else:
                    messagebox.showerror("Erro", "Saldo insuficiente.")
                break 
        
        if not user_found_sacar:
            messagebox.showerror("Erro", "Usuário não encontrado.")          


    confirm = tk.Button(action_frame, text="Confirmar", command=lambda: sacar2(cpf, users), font=BUTTON_FONT, width=12, height=2)
    confirm.pack(side=tk.LEFT, padx=10)
    tk.Button(action_frame, text="Voltar ao Menu", command=lambda: menu_usuario(cpf, users), font=BUTTON_FONT, width=15, height=2).pack(side=tk.RIGHT, padx=10)

def limpar_tela():
    for widget in root.winfo_children():
        widget.destroy()

root.mainloop()