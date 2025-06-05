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
    for widget in root.winfo_children():
        widget.destroy()
    
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
                for widget in root.winfo_children():
                    widget.destroy()
                menu_usuario(cpf, users)
                found = True
                break
        if found:
            break
    
    if not found:
        messagebox.showerror("Erro de Login", "CPF ou senha incorretos.")
                
    return cpf
                
def menu_usuario(cpf, users):
    for widget in root.winfo_children():
        widget.destroy()   
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
    for widget in root.winfo_children():
        widget.destroy()
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
        
        bytes = usuario['senha'].encode()
        usuario['senha'] = hashlib.sha256(bytes).hexdigest() 

        database = {CPF: usuario}
        users.append(database)
        
        try:
            content = json.dumps(users)
            path.write_text(content)
        except Exception as e:
            messagebox.showerror("Erro de Cadastro", f"Erro ao salvar dados do novo usuário: {e}")
            return

        bem_vindo(usuario)

        msg = tk.Label(root, text="Seu cadastro foi concluído com sucesso!", fg="green")
        msg.pack()

        cpf = CPF

        try:
            with open("user.json", "w") as file:
                json.dump(users, file, indent=4)
        except Exception as e:
            messagebox.showerror("Erro de Cadastro", f"Erro ao salvar dados do novo usuário: {e}")
            return

        menu_usuario(cpf, users)

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

        bytes = usuario['senha'].encode()
        usuario['senha'] = hashlib.sha256(bytes).hexdigest()

        database = {CPF: usuario}
        users = [database]
        
        try:
            content = json.dumps(users)
            path.write_text(content)
        except Exception as e:
            messagebox.showerror("Erro de Cadastro", f"Erro ao criar arquivo de usuários: {e}")
            return


        bem_vindo(usuario)

        msg = tk.Label(root, text="Seu cadastro foi concluído com sucesso!", fg="green")
        msg.pack()

        cpf = CPF

        try:
            with open("user.json", "w") as file:
                json.dump(users, file, indent=4)
        except Exception as e:
            messagebox.showerror("Erro de Cadastro", f"Erro ao salvar dados do novo usuário: {e}")
            return

        menu_usuario(cpf, users)

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
