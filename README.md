#Simulador de Caixa Eletrônico

Este é um projeto de Simulador de Caixa Eletrônico em Python com interface gráfica por Tkinter. O projeto simula um banco onde permite que os usuários façam as seguintes operações: Registro, Login, Redefinir a senha, Saque, depósito e Mostrar o saldo, tudo através do próprio código fazendo-se com o Tkinter e os dados do usuário é salvo em um arquivo JSON local. 

---

##Funcionalidades

- Cadastro de novos usuários com:
   - CPF
   - Nome completo
   - Idade
   - E-mail
   - Senha (armazenada de forma criptografada com SHA-256)
- Envio automático de e-mail de boas-vindas após o cadastro
- Login com CPF e senha
- Redefinição de senha com código de verificação enviado por e-mail
- Consulta de saldo
- Realização de depósitos
- Realização de saques
- Interface gráfica intuitiva desenvolvida com Tkinter

---

##Armazenamento de Dados

- Os dados dos usuários são armazenados no arquivo `user.json`, contendo:
   - CPF
   - Nome completo
   - Idade
   - E-mail
   - Senha criptografada (SHA-256)
   - Saldo atual

---

##Segurança

 - As senhas são protegidas utilizando criptografia SHA-256.
 - O processo de redefinição de senha exige um código de verificação enviado para o e-mail cadastrado.
 - Envio de e-mails implementado utilizando protocolo SMTP com conexão segura TLS.

---

##Tecnologias Utilizadas

 - Python
 - Tkinter (interface gráfica)
 - JSON (armazenamento local)
 - hashlib (criptografia de senha)
 - smtplib e email.message (envio de e-mails)

---

##Desenvolvedor

 - *José Gustavo Martinho Araújo de Almeida*
 - *João Gabriel Vasconcelos de Melo*
