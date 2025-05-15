# **MyServerManager - Configuração e Automação**

Este repositório contém scripts em Python para automatizar o gerenciamento das instancias e servidores (Zomboid e Minecraft) na AWS.

---

## **Requisitos**

Antes de começar, garanta que você tenha os seguintes requisitos:

- **AWS CLI**: A ferramenta de linha de comando da AWS deve estar instalada e configurada. 
- **Bibliotecas Python**: As dependências do projeto estão listadas no arquivo `requirements.txt`.

Para instalar as bibliotecas, execute:

```bash
pip install -r requirements.txt
```

## **Como Configurar**
Configurar AWS CLI: Após instalar a AWS CLI, execute aws configure e insira as credenciais da conta aws.

Configurar Variáveis no .env: Rode o main.py e selecione a opcao de gerar o .env do jogo que queres e depois informar o caminho da chave .PEM
Estrutura exemplo .env:
```plaintext
INSTANCE_ID   = "<ID da sua instância EC2>"
KEY_PATH      = "<Caminho para sua chave .pem>"
USER          = "ubuntu"
STOP_COMMAND  = "sudo systemctl start stop-zomboid.service"
START_COMMAND = "sudo systemctl start start-zomboid.service"
ACESS_COMMAND = "screen -r zomboid"

```

## **TO-DO**

1. Backup do save no S3;
2. Criar services para iniciar a instancia e iniciar automaticamente o servidor
3. Deixar menu bonito
