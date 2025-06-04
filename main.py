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
        widget.destroy() # Limpa a tela
    
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