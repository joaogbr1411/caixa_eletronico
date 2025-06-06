Com certeza! Baseado nos arquivos fornecidos, aqui está uma proposta de `README.md` completa e bem estruturada em português.

---

# Simulador de Caixa Eletrônico

Este projeto consiste em um simulador de caixa eletrônico (ATM) totalmente funcional, desenvolvido em Python. Ele oferece duas interfaces de usuário: uma gráfica (GUI) construída com Tkinter e uma de linha de comando (CLI). O sistema permite que usuários se cadastrem, realizem login, gerenciem suas finanças através de saques e depósitos, e recuperem suas senhas de forma segura.

## 🚀 Funcionalidades Principais

O simulador oferece uma gama completa de operações bancárias básicas:

-   **Interface Dupla**: O usuário pode interagir com o sistema através de uma interface gráfica intuitiva (`main.py`) ou por uma interface de linha de comando (`caixa_eletronico.py`).
-   **Cadastro de Usuários**: Novos usuários podem se registrar fornecendo CPF, nome completo, idade e e-mail.
-   **Login Seguro**: Autenticação de usuários por meio de CPF e senha.
-   **Gestão de Saldo**:
    -   Consulta de saldo atual.
    -   Realização de depósitos em conta.
    -   Realização de saques, com verificação de saldo disponível.
-   **Notificações por E-mail**:
    -   Envio de um e-mail de boas-vindas para o usuário logo após o cadastro bem-sucedido.
    -   Sistema de redefinição de senha que envia um código de verificação para o e-mail cadastrado, garantindo a identidade do usuário.

## 🛠️ Tecnologias Utilizadas

O projeto foi construído utilizando as seguintes tecnologias e bibliotecas Python:

-   **Python**: Linguagem base para toda a lógica do programa.
-   **Tkinter**: Para a construção da interface gráfica do usuário (GUI).
-   **JSON**: Utilizado para o armazenamento local dos dados dos usuários no arquivo `user.json`.
-   **hashlib**: Para a criptografia segura das senhas de usuário utilizando o algoritmo SHA-256.
-   **smtplib** e **email.message**: Para o envio de e-mails de boas-vindas e de recuperação de senha.
-   **pathlib**: Para manipulação de caminhos de arquivos de forma moderna e multiplataforma.

## 📂 Estrutura do Projeto

```
.
├── main.py                 # Arquivo principal para executar a versão com interface gráfica (Tkinter)
├── caixa_eletronico.py     # Arquivo para executar a versão de linha de comando (CLI)
├── user.json               # Arquivo de "banco de dados" que armazena os dados dos usuários
└── README.md               # Este arquivo
```

## 🔐 Segurança

A segurança é um pilar fundamental deste projeto, implementada através de:

-   **Criptografia de Senhas**: As senhas dos usuários nunca são armazenadas em texto plano. Elas são processadas com o algoritmo de hash SHA-256 antes de serem salvas no arquivo `user.json`.
-   **Recuperação de Senha Verificada**: O processo de redefinição de senha exige um código de verificação único, enviado para o e-mail do usuário, impedindo o acesso não autorizado.
-   **Comunicação Segura**: A conexão com o servidor de e-mail é protegida com o protocolo TLS (Transport Layer Security), garantindo que os dados de login e as mensagens sejam criptografados durante o envio.

## ⚙️ Como Executar

Para executar o simulador, siga os passos abaixo:

1.  **Pré-requisitos**: Certifique-se de ter o Python 3 instalado em sua máquina. As bibliotecas utilizadas são parte da biblioteca padrão do Python, não sendo necessária a instalação de pacotes externos.

2.  **Configuração de E-mail**:
    -   As funções de envio de e-mail estão configuradas para usar uma conta do Gmail.
    -   Para que funcione, você precisará alterar o e-mail e a senha no código (`sobek0955@gmail.com` e a senha associada) nos arquivos `main.py` e `caixa_eletronico.py`.
    -   **Importante**: O Gmail exige a criação de uma **"Senha de App"** para permitir que aplicações de terceiros façam login. Você deve gerar uma na configuração de segurança da sua Conta Google e usá-la no lugar da sua senha principal.

3.  **Execução**:
    -   **Para a Interface Gráfica (GUI)**: Abra um terminal na pasta do projeto e execute o comando:
        ```bash
        python main.py
        ```
    -   **Para a Interface de Linha de Comando (CLI)**: Abra um terminal e execute:
        ```bash
        python caixa_eletronico.py
        ```

## 👥 Desenvolvedores

Este projeto foi desenvolvido por:

-   José Gustavo Martinho Araújo de Almeida
-   João Gabriel Vasconcelos de Melo